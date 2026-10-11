
"""M3-T07/T08: PostgreSQL integration tests against a dedicated test DB."""

import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, inspect, select, text, update
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.db.models import (
    ProjectRow,
    TaskRow,
    WorkspaceMemberRow,
    WorkspaceRow,
)
from app.exceptions import (
    DbProjectAlreadyExistsError,
    TaskProjectWorkspaceMismatchError,
)
from app.repositories.workspaces import WorkspaceRepository
from app.services import (
    ProjectDbService,
    TaskDbService,
    UserDbService,
    WorkspaceDbService,
)

TEST_DB_NAME = "ai_workspace_lite_test"


@pytest.fixture(scope="session")
def db_engine():
    """Connect only to the explicitly selected M3 test database."""
    raw_url = os.getenv("TEST_DATABASE_URL")
    if not raw_url:
        pytest.skip("Set TEST_DATABASE_URL to run the PostgreSQL integration tests")

    url = make_url(raw_url)
    if url.drivername != "postgresql+psycopg" or url.database != TEST_DB_NAME:
        pytest.fail(
            "Refusing database tests: TEST_DATABASE_URL must use "
            f"postgresql+psycopg and database {TEST_DB_NAME!r}"
        )

    engine = create_engine(raw_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            current_name = connection.scalar(text("SELECT current_database()"))
            if current_name != TEST_DB_NAME:
                pytest.fail(f"Connected to unexpected database: {current_name}")

            expected_tables = {
                "alembic_version", "users", "workspaces", "workspace_members",
                "projects", "tasks", "files", "operation_logs",
            }
            missing = expected_tables - set(inspect(connection).get_table_names())
            if missing:
                pytest.fail(
                    "Run Alembic migrations on the test DB first. "
                    f"Missing tables: {sorted(missing)}"
                )
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db(db_engine):
    """Each test gets an isolated Session; all its changes are rolled back."""
    with db_engine.connect() as connection:
        outer_transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        )
        try:
            yield session, connection
        finally:
            session.close()
            outer_transaction.rollback()


@pytest.fixture
def owner(db):
    session, _ = db
    suffix = uuid4().hex[:12]
    return UserDbService(session).create_user(
        username=f"m3_{suffix}",
        email=f"m3_{suffix}@example.test",
    )


def make_workspace(session, owner_id, name="workspace_a"):
    return WorkspaceDbService(session).create_workspace(
        owner_user_id=owner_id,
        name=name,
    )


def make_project(session, workspace_id, name="paper"):
    return ProjectDbService(session).create_project(
        workspace_id=workspace_id,
        name=name,
        description="Test project",
    )


def make_task(session, workspace_id, title, *, project_id=None, status="todo"):
    return TaskDbService(session).create_task(
        workspace_id=workspace_id,
        project_id=project_id,
        title=title,
        description=None,
        status=status,
    )


def list_tasks(session, workspace_id, **changes):
    arguments = {
        "workspace_id": workspace_id,
        "status": None,
        "project_id": None,
        "limit": 20,
        "offset": 0,
        "sort_by": "created_at",
        "order": "desc",
    }
    arguments.update(changes)
    return TaskDbService(session).list_tasks(**arguments)


def test_create_workspace_also_creates_owner_membership(db, owner):
    session, connection = db
    workspace = make_workspace(session, owner.id)

    persisted_owner_id = connection.scalar(
        select(WorkspaceRow.owner_user_id).where(WorkspaceRow.id == workspace.id)
    )
    role = connection.scalar(
        select(WorkspaceMemberRow.role).where(
            WorkspaceMemberRow.workspace_id == workspace.id,
            WorkspaceMemberRow.user_id == owner.id,
        )
    )

    assert persisted_owner_id == owner.id
    assert role == "owner"


def test_workspace_rolls_back_when_member_creation_fails(db, owner, monkeypatch):
    session, connection = db
    created_ids = []

    def fail_add_member(repository, *, workspace_id, user_id, role):
        created_ids.append(workspace_id)
        # WorkspaceRepository.add() already flushed an INSERT in this transaction.
        assert connection.scalar(
            select(WorkspaceRow.id).where(WorkspaceRow.id == workspace_id)
        ) == workspace_id
        raise RuntimeError("forced membership failure")

    monkeypatch.setattr(WorkspaceRepository, "add_member", fail_add_member)

    with pytest.raises(RuntimeError, match="forced membership failure"):
        make_workspace(session, owner.id, name="rollback_workspace")

    assert len(created_ids) == 1
    assert connection.scalar(
        select(func.count()).select_from(WorkspaceRow).where(
            WorkspaceRow.id == created_ids[0]
        )
    ) == 0
    assert connection.scalar(
        select(func.count()).select_from(WorkspaceMemberRow).where(
            WorkspaceMemberRow.workspace_id == created_ids[0]
        )
    ) == 0


def test_duplicate_project_name_in_same_workspace_is_rejected(db, owner):
    session, connection = db
    workspace = make_workspace(session, owner.id)
    make_project(session, workspace.id, name="same_name")

    with pytest.raises(DbProjectAlreadyExistsError):
        make_project(session, workspace.id, name="same_name")

    assert connection.scalar(
        select(func.count()).select_from(ProjectRow).where(
            ProjectRow.workspace_id == workspace.id,
            ProjectRow.name == "same_name",
        )
    ) == 1


def test_task_cannot_reference_project_from_another_workspace(db, owner):
    session, connection = db
    first = make_workspace(session, owner.id, "workspace_first")
    second = make_workspace(session, owner.id, "workspace_second")
    project = make_project(session, first.id)

    with pytest.raises(TaskProjectWorkspaceMismatchError):
        make_task(session, second.id, "invalid cross-workspace task", project_id=project.id)

    assert connection.scalar(
        select(func.count()).select_from(TaskRow).where(
            TaskRow.workspace_id == second.id
        )
    ) == 0


def test_task_status_filter(db, owner):
    session, _ = db
    workspace = make_workspace(session, owner.id)
    make_task(session, workspace.id, "todo_1", status="todo")
    make_task(session, workspace.id, "done_1", status="done")
    make_task(session, workspace.id, "todo_2", status="todo")

    items, total = list_tasks(session, workspace.id, status="todo", sort_by="title", order="asc")
    assert total == 2
    assert [item.title for item in items] == ["todo_1", "todo_2"]
    assert all(item.status == "todo" for item in items)

    empty_items, empty_total = list_tasks(session, workspace.id, status="missing")
    assert empty_total == 0
    assert empty_items == []


def test_task_pagination_returns_page_and_unpaginated_total(db, owner):
    session, _ = db
    workspace = make_workspace(session, owner.id)
    for index in range(5):
        make_task(session, workspace.id, f"task_{index}")

    items, total = list_tasks(
        session, workspace.id, limit=2, offset=1, sort_by="title", order="asc"
    )
    assert total == 5
    assert [item.title for item in items] == ["task_1", "task_2"]

    beyond, total_beyond = list_tasks(
        session, workspace.id, limit=2, offset=5, sort_by="title", order="asc"
    )
    assert total_beyond == 5
    assert beyond == []


def test_task_sort_by_title(db, owner):
    session, _ = db
    workspace = make_workspace(session, owner.id)
    for title in ("charlie", "alpha", "bravo"):
        make_task(session, workspace.id, title)

    ascending, _ = list_tasks(session, workspace.id, sort_by="title", order="asc")
    descending, _ = list_tasks(session, workspace.id, sort_by="title", order="desc")
    assert [item.title for item in ascending] == ["alpha", "bravo", "charlie"]
    assert [item.title for item in descending] == ["charlie", "bravo", "alpha"]


def test_task_sort_by_created_at(db, owner):
    session, connection = db
    workspace = make_workspace(session, owner.id)
    tasks = {
        title: make_task(session, workspace.id, title)
        for title in ("late", "early", "middle")
    }
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for title, days in (("early", 0), ("middle", 1), ("late", 2)):
        connection.execute(
            update(TaskRow)
            .where(TaskRow.id == tasks[title].id)
            .values(created_at=base_time + timedelta(days=days))
        )

    ascending, _ = list_tasks(session, workspace.id, sort_by="created_at", order="asc")
    descending, _ = list_tasks(session, workspace.id, sort_by="created_at", order="desc")
    assert [item.title for item in ascending] == ["early", "middle", "late"]
    assert [item.title for item in descending] == ["late", "middle", "early"]


def test_task_list_joins_project_name_and_keeps_tasks_without_project(db, owner):
    session, _ = db
    workspace = make_workspace(session, owner.id)
    project = make_project(session, workspace.id, name="paper")
    make_task(session, workspace.id, "with_project", project_id=project.id)
    make_task(session, workspace.id, "without_project")

    items, total = list_tasks(session, workspace.id, sort_by="title", order="asc")
    assert total == 2
    by_title = {item.title: item for item in items}
    assert by_title["with_project"].project_id == project.id
    assert by_title["with_project"].project_name == "paper"
    assert by_title["without_project"].project_id is None
    assert by_title["without_project"].project_name is None

def test_title_contains_filter(db, owner):
    session, _ = db

    workspace = make_workspace(
        session,
        owner.id,
        "title_filter_workspace",
    )

    other_workspace = make_workspace(
        session,
        owner.id,
        "other_title_workspace",
    )

    make_task(
        session,
        workspace.id,
        "Run experiment",
        status="todo",
    )

    make_task(
        session,
        workspace.id,
        "EXPERIMENT setup",
        status="todo",
    )

    make_task(
        session,
        workspace.id,
        "Experiment finished",
        status="done",
    )

    make_task(
        session,
        workspace.id,
        "Write report",
        status="todo",
    )

    make_task(
        session,
        other_workspace.id,
        "Other experiment",
        status="todo",
    )

    items, total = list_tasks(
        session,
        workspace.id,
        status="todo",
        title_contains="experiment",
        limit=1,
    )

    # total 不受 limit=1 影响
    assert total == 2
    assert len(items) == 1

    all_items, total = list_tasks(
        session,
        workspace.id,
        status="todo",
        title_contains="EXPERIMENT",
    )

    # 不区分大小写
    assert total == 2
    assert {
        item.title for item in all_items
    } == {
        "Run experiment",
        "EXPERIMENT setup",
    }

    empty_items, empty_total = list_tasks(
        session,
        workspace.id,
        title_contains="not_existing_title",
    )

    assert empty_items == []
    assert empty_total == 0
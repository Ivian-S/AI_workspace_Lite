from pathlib import Path

import pytest

from app.exceptions import (
    ProjectNotFoundError,
    ProjectAlreadyExistsError,
)
from app.storage import (
    InMemoryProjectStorage,
    JsonProjectStorage,
)

from app.services import ProjectService 


def test_service_creates_and_stores_project() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    project = service.create_project(
        "AI Workspace Lite",
        description="backend learning project",
    )

    projects = service.list_projects()

    assert project.name == "AI Workspace Lite"
    assert project.description == "backend learning project"
    assert projects == [project]

def test_service_keeps_multiple_projects() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    first = service.create_project("first")
    second = service.create_project("second")

    assert service.list_projects() == [first, second]

def test_different_storages_have_independent_state() -> None:
    storage_a = InMemoryProjectStorage()
    storage_b = InMemoryProjectStorage()

    service_a = ProjectService(storage_a)
    service_b = ProjectService(storage_b)

    service_a.create_project("only-a")

    assert len(service_a.list_projects()) == 1
    assert service_b.list_projects() == []

def test_list_projects_does_not_expose_storage_list() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    service.create_project("demo")

    projects = service.list_projects()
    projects.clear()

    assert len(service.list_projects()) == 1

def test_get_project_by_name_success() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    project = service.create_project("demo")

    assert service.get_project("demo") == project

def test_get_project_raises_when_project_not_found() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    with pytest.raises(
        ProjectNotFoundError,
        match="Project not found: missing",
    ):
        service.get_project("missing")

def test_update_project_success(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    project = service.create_project("demo")

    updated_project = service.update_project(
        "demo",
        name="updated_demo",
        description="updated description",
        tags=["tag1", "tag2"],
        members=["user1", "user2"],
    )

    assert updated_project.name == "updated_demo"
  
def test_update_project_not_found(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    with pytest.raises(
        ProjectNotFoundError,
        match="Project not found: missing",
    ):
        service.update_project(
            "missing",
            name="updated_missing",
            description="updated description",
            tags=["tag1", "tag2"],
            members=["user1", "user2"],
        )
        

def test_update_missing_project_raises_not_found_before_name_conflict(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    service.create_project("existing")

    with pytest.raises(ProjectNotFoundError):
        service.update_project(
            "missing",
            name="existing",
            description=None,
            tags=[],
            members=[],
        )


def test_update_project_keeps_supplied_fields(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    service.create_project("demo")

    service.update_project(
        "demo",
        name="updated-demo",
        description="updated",
        tags=["python"],
        members=["alice"],
    )

    project = service.get_project("updated-demo")

    assert project.description == "updated"
    assert project.tags == ["python"]
    assert project.members == ["alice"]


def test_delete_project_success(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    project = service.create_project("demo")

    service.delete_project("demo")

    assert service.list_projects() == []

def test_delete_project_not_found(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    with pytest.raises(
        ProjectNotFoundError,
        match="Project not found: missing",
    ):
        service.delete_project("missing")

def test_create_project_repeated_name_raises_error(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )
    service = ProjectService(storage)

    service.create_project("demo")

    with pytest.raises(
        ProjectAlreadyExistsError,
        match="Project already exists: demo",
    ):
        service.create_project("demo")
# 新增：app/services.py

from app.exceptions import (
    ProjectNotFoundError,
    ProjectAlreadyExistsError,
)
from app.models import Project
from app.storage import (
    InMemoryProjectStorage,
    JsonProjectStorage,
)

# 新增：当前阶段的临时共同类型
ProjectStorage = InMemoryProjectStorage | JsonProjectStorage

class ProjectService:
    def __init__(
        self,
        storage: ProjectStorage,
    ) -> None:
        self._storage = storage

    def create_project(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
        members: list[str] | None = None,
    ) -> Project:

        # 检查项目是否存在
        if self._storage.get_by_name(name) is not None:
            raise ProjectAlreadyExistsError(name)

        project = Project(
            name=name,
            description=description,
            tags=[] if tags is None else list(tags),
            members=[] if members is None else list(members),
        )
        self._storage.save(project)
        return project
    
    def list_projects(self) -> list[Project]:
        return self._storage.list_all()

    def get_project(self, name: str) -> Project:
        project = self._storage.get_by_name(name)
        if project is None:
            raise ProjectNotFoundError(name)
        return project

    def update_project(
        self,
        current_name: str,
        *,
        name: str,
        description: str | None,
        tags: list[str],
        members: list[str],
    ) -> Project:

        current_project = self._storage.get_by_name(current_name)
        if current_project is None:
            raise ProjectNotFoundError(current_name)

        if (
            name != current_name
            and self._storage.get_by_name(name) is not None
        ):
            raise ProjectAlreadyExistsError(name)

        updated_project = Project(
            name=name,
            description=description,
            tags=list(tags),
            members=list(members),
        )

        updated = self._storage.update_by_name(
            current_name,
            updated_project,
        )

        if not updated:
            raise ProjectNotFoundError(current_name)

        return updated_project

    def delete_project(self, name: str) -> None:
        deleted = self._storage.delete_by_name(name)
        if not deleted:
            raise ProjectNotFoundError(name)



# ProjectService
#     │
#     ├── 理解“创建项目”这个业务动作
#     │
#     ├── 构造 Project
#     │
#     └── 要求 Storage 保存

# Storage
#     │
#     ├── 不决定 Project 应该有哪些业务规则
#     └── 只负责保存和读取

# 新增数据库业务Service
from sqlalchemy.orm import Session

from app.exceptions import (
    DbProjectAlreadyExistsError,
    DbProjectNotFoundError,
    TaskProjectWorkspaceMismatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
)

from app.repositories.projects import (
    ProjectRepository,
)
from app.repositories.tasks import (
    TaskListItem,
    TaskRepository,
)
from app.repositories.users import UserRepository
from app.repositories.workspaces import (
    WorkspaceRepository,
)

class UserDbService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._users = UserRepository(session)

    def create_user(
        self,
        *,
        username: str,
        email: str,
    ):
        with self._session.begin():
            if (
                self._users.get_by_username(
                    username
                )
                is not None
            ):
                raise UserAlreadyExistsError(
                    username
                )

            if (
                self._users.get_by_email(email)
                is not None
            ):
                raise UserAlreadyExistsError(
                    email
                )

            return self._users.add(
                username=username,
                email=email,
            )


class WorkspaceDbService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._users = UserRepository(session)
        self._workspaces = (
            WorkspaceRepository(session)
        )

    def create_workspace(
        self,
        *,
        owner_user_id: int,
        name: str,
    ):
        with self._session.begin():

            owner = self._users.get(
                owner_user_id
            )
            if owner is None:
                raise UserNotFoundError(
                    owner_user_id
                )

            existing = (
                self._workspaces
                .get_by_owner_and_name(
                    owner_user_id=owner_user_id,
                    name=name,
                )
            )

            if existing is not None:
                raise WorkspaceAlreadyExistsError(
                    name
                )

            workspace = self._workspaces.add(
                owner_user_id=owner_user_id,
                name=name,
            )

            self._workspaces.add_member(
                workspace_id=workspace.id,
                user_id=owner_user_id,
                role="owner",
            )

            return workspace

class ProjectDbService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._workspaces = (
            WorkspaceRepository(session)
        )
        self._projects = (
            ProjectRepository(session)
        )

    def create_project(
        self,
        *,
        workspace_id: int,
        name: str,
        description: str | None,
    ):
        with self._session.begin():

            workspace = self._workspaces.get(
                workspace_id
            )

            if workspace is None:
                raise WorkspaceNotFoundError(
                    workspace_id
                )

            existing = (
                self._projects
                .get_by_workspace_and_name(
                    workspace_id=workspace_id,
                    name=name,
                )
            )

            if existing is not None:
                raise DbProjectAlreadyExistsError(
                    name
                )

            return self._projects.add(
                workspace_id=workspace_id,
                name=name,
                description=description,
            )

class TaskDbService:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._workspaces = (
            WorkspaceRepository(session)
        )
        self._projects = (
            ProjectRepository(session)
        )
        self._tasks = TaskRepository(session)

    def create_task(
        self,
        *,
        workspace_id: int,
        project_id: int | None,
        title: str,
        description: str | None,
        status: str,
    ):
        with self._session.begin():

            workspace = self._workspaces.get(
                workspace_id
            )

            if workspace is None:
                raise WorkspaceNotFoundError(
                    workspace_id
                )

            if project_id is not None:
                project = self._projects.get(
                    project_id
                )

                if project is None:
                    raise DbProjectNotFoundError(
                        project_id
                    )

                if (
                    project.workspace_id
                    != workspace_id
                ):
                    raise (
                        TaskProjectWorkspaceMismatchError(
                            project_id
                        )
                    )

            return self._tasks.add(
                workspace_id=workspace_id,
                project_id=project_id,
                title=title,
                description=description,
                status=status,
            )

    def list_tasks(
        self,
        *,
        workspace_id: int,
        status: str | None,
        project_id: int | None,
        limit: int,
        offset: int,
        sort_by: str,
        order: str,
        title_contains: str | None = None,
    ) -> tuple[list[TaskListItem], int]:

        if (
            self._workspaces.get(workspace_id)
            is None
        ):
            raise WorkspaceNotFoundError(
                workspace_id
            )

        return self._tasks.list_for_workspace(
            workspace_id=workspace_id,
            status=status,
            project_id=project_id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            title_contains=title_contains,
        )
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

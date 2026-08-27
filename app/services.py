# 新增：app/services.py

from app.models import Project
from app.storage import InMemoryProjectStorage
from app.exceptions import ProjectNotFoundError


class ProjectService:
    def __init__(
        self,
        storage: InMemoryProjectStorage,
    ) -> None:
        self._storage = storage

    def create_project(
        self,
        name: str,
        description: str | None = None,
        tags: list[str] | None = None,
        members: list[str] | None = None,
    ) -> Project:
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

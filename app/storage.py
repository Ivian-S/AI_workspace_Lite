# 新增：app/storage.py

from app.models import Project

class InMemoryProjectStorage:

    # 初始化项目存储
    def __init__(self) -> None:
        self._projects: list[Project] = []

    def save(self, project: Project) -> None:
        self._projects.append(project)

    # 列出所有项目，如果直接返回内部列表，会导致外部修改列表，所以返回一个副本
    def list_all(self) -> list[Project]:
        return list(self._projects)

    def get_by_name(self, name: str) -> Project | None:
        for project in self._projects:
            if project.name == name:
                return project
        return None

# 前面的 _ 不是安全机制。

# 它表达的是：

# > 这是模块/类内部实现细节，调用者通常不应该直接操作。

# Python 并不会禁止：
# storage._projects

# 这是一种约定。

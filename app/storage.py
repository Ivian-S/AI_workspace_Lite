# 新增：app/storage.py

import json
from dataclasses import asdict
from pathlib import Path

from app.exceptions import ProjectStorageDataError
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

    def update_by_name(
        self,
        name: str,
        updated_project: Project,
    ) -> bool:
        for index, project in enumerate(self._projects):
            if project.name == name:
                self._projects[index] = updated_project
                return True
        return False

    def delete_by_name(self, name: str) -> bool:
        for index, project in enumerate(self._projects):
            if project.name == name:
                del self._projects[index]
                return True
        return False

class JsonProjectStorage:

    def __init__(self, file_path: str |Path) -> None:
        self._file_path = Path(file_path)

    def _load(self) -> list[Project]:
        if not self._file_path.exists():
            return []

        text = self._file_path.read_text(encoding="utf-8")
        if not text.strip():
            return []

        try:
            raw_projects = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ProjectStorageDataError(str(self._file_path)) from exc

        if not isinstance(raw_projects, list):
            raise ProjectStorageDataError(str(self._file_path))
        
        projects: list[Project] = []
        for raw_project in raw_projects:
            if not isinstance(raw_project, dict):
                raise ProjectStorageDataError(str(self._file_path))
            
            try:
                project = Project(**raw_project)
            except TypeError as exc:
                raise ProjectStorageDataError(str(self._file_path)) from exc
            projects.append(project)

        return projects

    def _write(self,projects: list[Project],) -> None:
        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        raw_projects = [
            asdict(project)
            for project in projects
        ]

        text = json.dumps(
            raw_projects,
            ensure_ascii=False,
            indent=2,
        )

        self._file_path.write_text(
            text + "\n",
            encoding="utf-8",
        )

    def save(self, project: Project) -> None:
        projects = self._load()
        projects.append(project)
        self._write(projects)

    def list_all(self) -> list[Project]:
        return self._load()

    def get_by_name(self, name: str) -> Project | None:
        for project in self._load():
            if project.name == name:
                return project
        return None

    def update_by_name(
        self,
        name: str,
        updated_project: Project,
    ) -> bool:
        projects = self._load()
        for index, project in enumerate(projects):
            if project.name == name:
                projects[index] = updated_project
                self._write(projects)
                return True
        return False

    def delete_by_name(self, name: str) -> bool:
        projects = self._load()
        for index, project in enumerate(projects):
            if project.name == name:
                del projects[index]
                self._write(projects)
                return True
        return False

# 前面的 _ 不是安全机制。

# 它表达的是：

# > 这是模块/类内部实现细节，调用者通常不应该直接操作。

# Python 并不会禁止：
# storage._projects

# 这是一种约定。

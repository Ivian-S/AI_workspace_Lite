# 新增业务异常类

class ProjectNotFoundError(Exception):
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        super().__init__(f"Project not found: {project_name}")

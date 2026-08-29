# 新增业务异常类

# 查询项目不存在异常类
class ProjectNotFoundError(Exception):
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        super().__init__(f"Project not found: {project_name}")

# 新增项目已存在异常类
class ProjectAlreadyExistsError(Exception):
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        super().__init__(f"Project already exists: {project_name}")

# 项目存储数据异常类
class ProjectStorageDataError(Exception):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        super().__init__(f"Invalid project storage data: {file_path}")

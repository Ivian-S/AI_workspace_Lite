# 新增：app/project_snapshot.py

from copy import deepcopy
from typing import Any


ProjectData = dict[str, Any]



def create_project_snapshot(project: ProjectData) -> ProjectData:
    """返回可安全交给调用方修改的项目数据副本。"""
    return deepcopy(project)
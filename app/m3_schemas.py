from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=64,
    )
    email: str = Field(
        min_length=3,
        max_length=320,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class WorkspaceCreateRequest(BaseModel):
    owner_user_id: int
    name: str = Field(
        min_length=1,
        max_length=200,
    )


class WorkspaceResponse(BaseModel):
    id: int
    owner_user_id: int
    name: str


class DbProjectCreateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200,
    )
    description: str | None = None


class DbProjectResponse(BaseModel):
    id: int
    workspace_id: int
    name: str
    description: str | None


class TaskCreateRequest(BaseModel):
    project_id: int | None = None
    title: str = Field(
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    status: str = Field(
        default="todo",
        min_length=1,
        max_length=32,
    )


class TaskResponse(BaseModel):
    id: int
    workspace_id: int
    project_id: int | None
    title: str
    description: str | None
    status: str


class TaskListItemResponse(TaskResponse):
    project_name: str | None
    created_at: datetime


class TaskListResponse(BaseModel):
    items: list[TaskListItemResponse]
    total: int
    limit: int
    offset: int


TaskSortBy = Literal[
    "created_at",
    "title",
    "status",
]

SortOrder = Literal["asc", "desc"]
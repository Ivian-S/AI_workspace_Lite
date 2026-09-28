from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    owned_workspaces: Mapped[list[WorkspaceRow]] = relationship(
        back_populates="owner",
    )
    memberships: Mapped[list[WorkspaceMemberRow]] = relationship(
        back_populates="user",
    )
    uploaded_files: Mapped[list[FileRow]] = relationship(
        back_populates="uploaded_by",
    )
    operation_logs: Mapped[list[OperationLogRow]] = relationship(
        back_populates="actor",
    )


class WorkspaceRow(Base):
    __tablename__ = "workspaces"
    __table_args__ = (
        UniqueConstraint(
            "owner_user_id",
            "name",
            name="uq_workspaces_owner_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    owner: Mapped[UserRow] = relationship(
        back_populates="owned_workspaces",
    )
    memberships: Mapped[list[WorkspaceMemberRow]] = relationship(
        back_populates="workspace",
    )
    projects: Mapped[list[ProjectRow]] = relationship(
        back_populates="workspace",
    )
    tasks: Mapped[list[TaskRow]] = relationship(
        back_populates="workspace",
    )
    files: Mapped[list[FileRow]] = relationship(
        back_populates="workspace",
    )
    operation_logs: Mapped[list[OperationLogRow]] = relationship(
        back_populates="workspace",
    )


class WorkspaceMemberRow(Base):
    __tablename__ = "workspace_members"

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(
        String(32),
        default="member",
        server_default="member",
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    workspace: Mapped[WorkspaceRow] = relationship(
        back_populates="memberships",
    )
    user: Mapped[UserRow] = relationship(
        back_populates="memberships",
    )


class ProjectRow(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "name",
            name="uq_projects_workspace_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    workspace: Mapped[WorkspaceRow] = relationship(
        back_populates="projects",
    )
    tasks: Mapped[list[TaskRow]] = relationship(
        back_populates="project",
    )


class TaskRow(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(32),
        default="todo",
        server_default="todo",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    workspace: Mapped[WorkspaceRow] = relationship(
        back_populates="tasks",
    )
    project: Mapped[ProjectRow | None] = relationship(
        back_populates="tasks",
    )


class FileRow(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )
    uploaded_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )
    content_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    size_bytes: Mapped[int] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    workspace: Mapped[WorkspaceRow] = relationship(
        back_populates="files",
    )
    uploaded_by: Mapped[UserRow] = relationship(
        back_populates="uploaded_files",
    )


class OperationLogRow(Base):
    __tablename__ = "operation_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    workspace_id: Mapped[int | None] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=True,
    )
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    resource_id: Mapped[int | None] = mapped_column(
        nullable=True,
    )
    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    workspace: Mapped[WorkspaceRow | None] = relationship(
        back_populates="operation_logs",
    )
    actor: Mapped[UserRow | None] = relationship(
        back_populates="operation_logs",
    )

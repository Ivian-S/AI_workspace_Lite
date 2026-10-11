from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import ProjectRow, TaskRow


@dataclass(frozen=True, slots=True)
class TaskListItem:
    id: int
    workspace_id: int
    project_id: int | None
    project_name: str | None
    title: str
    description: str | None
    status: str
    created_at: datetime


class TaskRepository:
    SORT_COLUMNS = {
        "created_at": TaskRow.created_at,
        "title": TaskRow.title,
        "status": TaskRow.status,
    }

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        *,
        workspace_id: int,
        project_id: int | None,
        title: str,
        description: str | None,
        status: str,
    ) -> TaskRow:
        task = TaskRow(
            workspace_id=workspace_id,
            project_id=project_id,
            title=title,
            description=description,
            status=status,
        )

        self._session.add(task)
        self._session.flush()

        return task

    def list_for_workspace(
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

        filters = [
            TaskRow.workspace_id == workspace_id
        ]

        if status is not None:
            filters.append(
                TaskRow.status == status
            )

        if project_id is not None:
            filters.append(
                TaskRow.project_id == project_id
            )

            # 新增：标题包含筛选
        if title_contains is not None:
            escaped_title = (
                title_contains
                .replace("/", "//")
                .replace("%", "/%")
                .replace("_", "/_")
            )

            filters.append(
                TaskRow.title.ilike(
                    f"%{escaped_title}%",
                    escape="/",
                )
            )

        count_stmt = (
            select(func.count(TaskRow.id))
            .where(*filters)
        )

        total = (
            self._session.scalar(count_stmt)
            or 0
        )

        sort_column = self.SORT_COLUMNS[
            sort_by
        ]

        order_expression = (
            sort_column.desc()
            if order == "desc"
            else sort_column.asc()
        )

        stmt = (
            select(
                TaskRow.id,
                TaskRow.workspace_id,
                TaskRow.project_id,
                ProjectRow.name.label(
                    "project_name"
                ),
                TaskRow.title,
                TaskRow.description,
                TaskRow.status,
                TaskRow.created_at,
            )
            .outerjoin(
                ProjectRow,
                TaskRow.project_id
                == ProjectRow.id,
            )
            .where(*filters)
            .order_by(
                order_expression,
                TaskRow.id,
            )
            .limit(limit)
            .offset(offset)
        )

        rows = self._session.execute(
            stmt
        ).all()

        items = [
            TaskListItem(
                id=row.id,
                workspace_id=row.workspace_id,
                project_id=row.project_id,
                project_name=row.project_name,
                title=row.title,
                description=row.description,
                status=row.status,
                created_at=row.created_at,
            )
            for row in rows
        ]

        return items, total
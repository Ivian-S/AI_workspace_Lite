from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ProjectRow


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(
        self,
        project_id: int,
    ) -> ProjectRow | None:
        return self._session.get(
            ProjectRow,
            project_id,
        )

    def get_by_workspace_and_name(
        self,
        *,
        workspace_id: int,
        name: str,
    ) -> ProjectRow | None:
        stmt = select(ProjectRow).where(
            ProjectRow.workspace_id
            == workspace_id,
            ProjectRow.name == name,
        )
        return self._session.scalar(stmt)

    def add(
        self,
        *,
        workspace_id: int,
        name: str,
        description: str | None,
    ) -> ProjectRow:
        project = ProjectRow(
            workspace_id=workspace_id,
            name=name,
            description=description,
        )
        self._session.add(project)
        self._session.flush()

        return project
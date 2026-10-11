from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import (
    WorkspaceMemberRow,
    WorkspaceRow,
)


class WorkspaceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(
        self,
        workspace_id: int,
    ) -> WorkspaceRow | None:
        return self._session.get(
            WorkspaceRow,
            workspace_id,
        )

    def get_by_owner_and_name(
        self,
        *,
        owner_user_id: int,
        name: str,
    ) -> WorkspaceRow | None:
        stmt = select(WorkspaceRow).where(
            WorkspaceRow.owner_user_id
            == owner_user_id,
            WorkspaceRow.name == name,
        )
        return self._session.scalar(stmt)

    def add(
        self,
        *,
        owner_user_id: int,
        name: str,
    ) -> WorkspaceRow:
        workspace = WorkspaceRow(
            owner_user_id=owner_user_id,
            name=name,
        )
        self._session.add(workspace)

        # membership 需要 workspace.id
        self._session.flush()

        return workspace

    def add_member(
        self,
        *,
        workspace_id: int,
        user_id: int,
        role: str,
    ) -> WorkspaceMemberRow:
        membership = WorkspaceMemberRow(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )
        self._session.add(membership)
        self._session.flush()

        return membership
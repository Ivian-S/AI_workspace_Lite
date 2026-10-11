from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import UserRow


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, user_id: int) -> UserRow | None:
        return self._session.get(UserRow, user_id)

    def get_by_username(
        self,
        username: str,
    ) -> UserRow | None:
        stmt = select(UserRow).where(
            UserRow.username == username
        )
        return self._session.scalar(stmt)

    def get_by_email(
        self,
        email: str,
    ) -> UserRow | None:
        stmt = select(UserRow).where(
            UserRow.email == email
        )
        return self._session.scalar(stmt)

    def add(
        self,
        *,
        username: str,
        email: str,
    ) -> UserRow:
        user = UserRow(
            username=username,
            email=email,
        )
        self._session.add(user)
        self._session.flush()
        return user
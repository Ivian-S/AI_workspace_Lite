import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg:///ai_workspace_lite",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
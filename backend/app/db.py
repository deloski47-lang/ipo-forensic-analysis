from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=4)
def _engine_for_path(database_path: str) -> Engine:
    return create_engine(
        f"sqlite:///{database_path.replace(chr(92), '/')}",
        connect_args={"check_same_thread": False},
    )


def get_engine() -> Engine:
    return _engine_for_path(str(get_settings().database_path))


def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()

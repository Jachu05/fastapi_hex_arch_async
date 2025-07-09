from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import atexit
import logging

from app.domain.models import Task
from app.ports.repositories import TaskRepository

Base = declarative_base()

# ---------------------------------------------------------------------------
# Engine and Session factory are created once at module import time so that
# every repository instance (and every request) re-uses the same *file-backed*
# SQLite database so we avoid race conditions on table creation.
# ---------------------------------------------------------------------------

_ENGINE = create_engine(
    "sqlite:///./tasks.db",
    connect_args={"check_same_thread": False},
    future=True,
    echo=False,
)

_SessionFactory: sessionmaker[Session] = sessionmaker(
    bind=_ENGINE,
    autoflush=False,
    autocommit=False,
    future=True,
)


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)

# After TaskORM is defined, ensure the table exists (only once).
Base.metadata.create_all(_ENGINE, checkfirst=True)

# ---------------------------------------------------------------------------
# Cleanup: wipe *all rows* from the SQLite file once the Python process
# terminates. This keeps the repository truly *ephemeral* so running the web
# app locally, the async client demo or the test-suite does not leave stale
# data on disk while still avoiding the threading issues of SQLite’s in-memory
# mode.
# ---------------------------------------------------------------------------


def _clear_tasks_table() -> None:  # pragma: no cover – executed only at shutdown
    """Remove all rows from the tasks table at interpreter shutdown."""

    try:
        with _SessionFactory() as session:
            session.execute(text("DELETE FROM tasks"))
            session.commit()
            logging.info("Cleared all rows from 'tasks' table at shutdown.")
    except Exception as exc:  # noqa: BLE001 – best-effort cleanup
        logging.getLogger(__name__).warning(
            "Failed to clear tasks table at shutdown: %s", exc,
        )


# Ensure the cleanup runs exactly once when the Python interpreter exits.
atexit.register(_clear_tasks_table)


class SQLiteTaskRepository(TaskRepository):
    """SQLite **file-backed** implementation of ``TaskRepository``.

    The repository stores data in a local ``tasks.db`` SQLite file that is
    automatically *cleared* (all rows deleted) when the Python interpreter
    exits.  This approach allows multiple threads to share the same database
    connection safely while still leaving the developer’s machine clean after
    each run – effectively emulating an *ephemeral* database without the
    cross-thread limitations of SQLite’s in-memory mode.
    """

    def __init__(self) -> None:
        # Each repository instance reuses the module-level session factory.
        self._Session = _SessionFactory

    def _session(self) -> Session:
        return self._Session()

    def add(self, description: str) -> Task:
        with self._session() as session:
            task_orm = TaskORM(description=description)
            session.add(task_orm)
            session.commit()
            session.refresh(task_orm)
            return Task(id=task_orm.id, description=task_orm.description)

    def get(self, task_id: int) -> Task:
        with self._session() as session:
            task_orm: Optional[TaskORM] = session.get(TaskORM, task_id)
            if task_orm is None:
                raise KeyError(f"Task with id {task_id} not found")
            return Task(id=task_orm.id, description=task_orm.description)

    def list(self) -> List[Task]:
        with self._session() as session:
            tasks_orm = session.query(TaskORM).all()
            return [Task(id=t.id, description=t.description) for t in tasks_orm]

    def delete(self, task_id: int) -> None:
        with self._session() as session:
            task_orm = session.get(TaskORM, task_id)
            if task_orm is None:
                raise KeyError(f"Task with id {task_id} not found")
            session.delete(task_orm)
            session.commit() 
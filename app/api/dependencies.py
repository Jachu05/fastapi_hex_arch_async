from functools import lru_cache

from app.adapters.repositories.sqlite_repository import SQLiteTaskRepository
from app.usecases.task_service import TaskService


"""FastAPI dependency helpers used across the API layer."""

@lru_cache
def get_task_service() -> TaskService:
    """Get application-wide singleton TaskService instance."""

    repository = SQLiteTaskRepository()
    return TaskService(repository) 
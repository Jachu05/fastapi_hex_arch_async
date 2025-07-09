from typing import List

from app.domain.models import Task
from app.ports.repositories import TaskRepository


class TaskService:
    """Application **service layer** orchestrating domain operations.

    The public methods expose *async* signatures so that FastAPI handlers can
    `await` them naturally.  Internally the work is executed synchronously – a
    pragmatic trade-off given SQLite’s lack of a stable async driver.
    """

    def __init__(self, repository: TaskRepository):
        self._repository = repository

    async def create_task(self, description: str) -> Task:
        return self._repository.add(description)

    async def get_task(self, task_id: int) -> Task:
        return self._repository.get(task_id)

    async def list_tasks(self) -> List[Task]:
        return self._repository.list()

    async def delete_task(self, task_id: int) -> None:
        self._repository.delete(task_id) 
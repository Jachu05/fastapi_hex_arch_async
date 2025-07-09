from abc import ABC, abstractmethod
from typing import List

from app.domain.models import Task


class TaskRepository(ABC):
    """Port describing repository operations for Task persistence."""

    @abstractmethod
    def add(self, description: str) -> Task:
        """Persist a new task"""

    @abstractmethod
    def get(self, task_id: int) -> Task:
        """Retrieve a task by id"""

    @abstractmethod
    def list(self) -> List[Task]:
        """Return all tasks"""

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """Delete a task by id""" 
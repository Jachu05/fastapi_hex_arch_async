from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    """Payload for creating a new task."""

    description: str


class TaskResponse(BaseModel):
    """Representation of a persisted task returned to clients."""

    id: int
    description: str 
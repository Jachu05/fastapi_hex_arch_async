from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Task:
    """Immutable domain entity representing a **to-do** task.

    Parameters
    ----------
    id:
        Unique identifier assigned by the persistence layer.
    description:
        Short textual description provided by the user.
    """
    id: int
    description: str 
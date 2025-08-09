from dataclasses import dataclass
from datetime import datetime

from src.domain.value_objects import TaskStatus


@dataclass(frozen=False)
class Task:
    task_id: int
    start_date: datetime | None
    error: str | None
    status: TaskStatus = TaskStatus.PENDING

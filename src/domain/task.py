from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=False)
class Task:
    task_id: int
    start_date: datetime | None
    error: str | None

from src.domain.entities.task import Task
from src.infrastructure.persistance.models import SqlServerTaskModel


class ToTask:

    def __rmatmul__(self, task_dto: SqlServerTaskModel) -> Task:
        return Task(task_id=task_dto.task_id, start_date=task_dto.start_date, error=task_dto.error)

from src.domain.task import Task
from src.infrastructure.models.task_model import TaskModel


class toTask:

    def __rmatmul__(self, task_dto: TaskModel) -> Task:
        return Task(task_id=task_dto.task_id, start_date=task_dto.start_date, error=task_dto.error)

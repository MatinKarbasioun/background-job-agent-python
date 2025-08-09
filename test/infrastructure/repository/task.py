from src.domain import Task
from src.domain.repositories import ITaskRepository


class MockTaskRepository(ITaskRepository):

    def __init__(self):
        self.not_found = "not found"
        self.some_job_id = "job id"
        self.task_count = 100
        self.some_open_task = Task(task_id=1,
                              start_date=None,
                              error=None)
        self.some_another_open_task = Task(task_id=2,
                                           start_date=None,
                                           error=None)

    async def is_exist(self, job_id: str) -> bool:
        if job_id != self.not_found:
            return True

        else:
            return False

    async def task_count(self, job_id: str) -> int:
        return self.task_count

    async def get_open_tasks(self, job_id: str, offset: int, limit: int) -> list[Task]:
        return [self.some_open_task, self.some_another_open_task]

    async def update_task(self, task: Task):
        pass

    @classmethod
    def task_repo(cls, session) -> 'ITaskRepository':
        pass
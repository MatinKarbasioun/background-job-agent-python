from abc import ABC, abstractmethod

from src.domain import Task


class ITaskRepository(ABC):

    @abstractmethod
    async def is_exist(self, job_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def task_count(self, job_id: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_open_tasks(self, job_id: str, offset: int, limit: int) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task):
        raise NotImplementedError

    @classmethod
    def task_repo(cls, session) -> 'ITaskRepository':
        raise NotImplementedError
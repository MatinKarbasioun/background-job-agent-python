from abc import ABC, abstractmethod

from src.domain import Task


class ITaskRepository(ABC):

    @abstractmethod
    async def get_open_tasks(self, batch_key: str):
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task):
        raise NotImplementedError

    @classmethod
    def task_repo(cls, session) -> 'ITaskRepository':
        raise NotImplementedError
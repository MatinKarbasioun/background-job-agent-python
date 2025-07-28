from abc import ABC, abstractmethod

from src.domain import Task


class ITaskClient(ABC):

    @abstractmethod
    async def start_task(self, task_id: int) -> Task:
        raise NotImplementedError

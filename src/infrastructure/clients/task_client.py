from abc import ABC, abstractmethod

from src.infrastructure.clients.task_response import TaskResponse


class ITaskClient(ABC):

    @abstractmethod
    async def start_task(self, task_id: int) -> TaskResponse:
        raise NotImplementedError

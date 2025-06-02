from abc import ABC, abstractmethod

from src.domain import Task


class ITaskClient(ABC):

    @abstractmethod
    def start_task(self, task: Task):
        raise NotImplementedError

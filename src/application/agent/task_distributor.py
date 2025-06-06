import asyncio
from typing import Any

from pykka import ThreadingActor
from asyncio import Queue

from src.application.agent.message.start_job import StartJobCommand
from src.application.agent.operator import TaskOperator
from src.application.task.task_handler import TaskHandler


class TaskDistributor(ThreadingActor):
    def __init__(self):
        super().__init__()
        self._task_handler = TaskHandler()
        self._task_operators = {}
        self._loop = asyncio.get_event_loop()

    def on_receive(self, msg: Any):
        asyncio.run_coroutine_threadsafe(self.async_on_receive(msg), self._loop)

    async def async_on_receive(self, msg: Any):
        if isinstance(msg, StartJobCommand):
            self.create_agents(msg.key)

    def create_agents(self, key):
        task_operator = TaskOperator.start(key)
        self._task_operators.update({key: task_operator})

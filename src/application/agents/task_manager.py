import asyncio
from typing import Any

from pykka import ThreadingActor

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StopJobCommand
from src.application.agents.messages.start_job import StartJobCommand
from src.application.agents.task_runner import TaskRunner
from src.application.service import TaskService


class TaskManager(ThreadingActor):
    def __init__(self):
        super().__init__()
        self._task_handler = TaskService()
        self._task_operators = {}
        self._loop = ActorSystem.event_loop
        asyncio.set_event_loop(self._loop)

    def on_receive(self, msg: Any):
        asyncio.run_coroutine_threadsafe(self.async_on_receive(msg), self._loop)

    async def async_on_receive(self, msg: Any):
        if isinstance(msg, StartJobCommand):
            self.create_runner(msg.task_id)

        elif isinstance(msg, StopJobCommand):
            self.stop_runner(msg.task_id)

    def create_runner(self, key):
        if not self._task_operators.get(key, None):
            task_operator = TaskRunner.start(key)
            self._task_operators.update({key: task_operator})

    def stop_runner(self, key):
        task_operator = self._task_operators.get(key, None)
        if task_operator:
            task_operator.stop()

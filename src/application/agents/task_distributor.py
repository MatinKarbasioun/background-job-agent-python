import asyncio
from typing import Any

from pykka import ThreadingActor

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages.start_job import StartJobCommand
from src.application.agents.operator import TaskOperator
from src.application.task.task_handler import TaskHandler


class TaskDistributor(ThreadingActor):
    def __init__(self):
        super().__init__()
        self._task_handler = TaskHandler()
        self._task_operators = {}
        self._loop = ActorSystem.event_loop
        asyncio.set_event_loop(self._loop)

    def on_receive(self, msg: Any):
        asyncio.run_coroutine_threadsafe(self.async_on_receive(msg), self._loop)

    async def async_on_receive(self, msg: Any):
        if isinstance(msg, StartJobCommand):
            self.create_agents(msg.key)

    def create_agents(self, key):
        if not self._task_operators.get(key, None):
            task_operator = TaskOperator.start(key)
            self._task_operators.update({key: task_operator})

    def stop_agent(self, key):
        task_operator = self._task_operators.get(key, None)
        if task_operator:
            task_operator.stop()

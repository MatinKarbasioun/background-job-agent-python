import asyncio
import time
from typing import Any

import pykka
from pykka import ThreadingActor

from src.application.agent.message import StartJobCommand, StopJobCommand
from src.application.agent.message.time import AddActorMessage, TimeSignal
from src.application.agent.time.timer import TimerAgent
from src.application.task.distributor import Distributor
from src.application.task.task_handler import TaskHandler


class TaskOperator(ThreadingActor):
    def __init__(self, key: str):
        super().__init__()
        self._key = key
        self._timer: pykka.ActorRef = TimerAgent.start()
        self._task_handler = TaskHandler()
        self._loop = asyncio.get_event_loop()
        self._distributor = Distributor(config={"duration":100})
        self._duration = 100
        self._offset = 0
        self._batch_size = 1
        self._cancellation_task = False
        self._loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.initialize(), self._loop)

    def on_receive(self, msg: Any):
        asyncio.run_coroutine_threadsafe(self.async_on_receive(msg), self._loop)

    async def async_on_receive(self, msg):
        if isinstance(msg, TimeSignal):
            await self._run()

        elif isinstance(msg, StopJobCommand):
            self._cancellation_task = True
            self.stop_task()

    async def initialize(self):
        task_count = await self._task_handler.task_count(self._key)
        self._batch_size = self._distributor.calculate(task_count)
        await self.setup_next_task()


    async def _run(self):

        if not self._cancellation_task:
            async for task in self._task_handler.get_open_tasks(task_key=self._key, batch_size=self._batch_size, offset=self._offset):
                await self._task_handler.start_task(task)

    async def setup_next_task(self):
        self._timer.tell(AddActorMessage(actor=self.actor_ref, startTime=time.time() + self._duration))

    def stop_task(self):
        self._cancellation_task = True
        self.stop()

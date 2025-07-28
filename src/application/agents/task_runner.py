import asyncio
import time
from typing import Any

from pykka import ThreadingActor

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StopJobCommand
from src.application.agents.messages.time import AddActorMessage, TimeSignal, StopTimerCommand
from src.application.app_setting import AppSetting
from src.application.task.distributor import Distributor
from src.application.service import TaskService
from src.application.time.job_time_service import JobDateTimeService
from src.domain import Task


class TaskRunner(ThreadingActor):
    def __init__(self, task: Task):
        super().__init__()
        self._task = task
        self._read_conf()

        self._task_service = TaskService()

        self._offset = 0
        self._batch_size = 1
        self._cancellation_task = False
        self._loop = ActorSystem.event_loop
        asyncio.set_event_loop(self._loop)
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
        task_count = await self._task_service.task_count(self._key)
        self._batch_size = self._distributor.calculate(task_count)
        await self.setup_next_task()

    async def _run(self):

        if not self._cancellation_task:
            if await self._task_service.is_exist(self._key):

                if self._time_service.is_running_time():
                    async for task in self._task_service.get_open_tasks(task_key=self._key, batch_size=self._batch_size, offset=self._offset):
                        await self._task_service.start_task(task)

            else:
                self.stop()

    def stop_task(self):
        self._cancellation_task = True
        self.stop()

    def on_stop(self) -> None:
        ActorSystem.timer_ref.tell(StopTimerCommand(self.actor_ref))

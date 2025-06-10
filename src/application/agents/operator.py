import asyncio
import time
from typing import Any

import pykka
from pykka import ThreadingActor

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StopJobCommand
from src.application.agents.messages.time import AddActorMessage, TimeSignal, StopTimerCommand
from src.application.agents.time.timer import TimerAgent
from src.application.app_setting import AppSetting
from src.application.task.distributor import Distributor
from src.application.task.task_handler import TaskHandler
from src.application.time.job_time_service import JobDateTimeService


class TaskOperator(ThreadingActor):
    def __init__(self, key: str):
        super().__init__()
        self._key = key
        self._read_conf()

        self._task_handler = TaskHandler()

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
        task_count = await self._task_handler.task_count(self._key)
        self._batch_size = self._distributor.calculate(task_count)
        await self.setup_next_task()

    async def _run(self):

        if not self._cancellation_task:
            if await self._task_handler.is_exist(self._key):

                if self._time_service.is_running_time():
                    async for task in self._task_handler.get_open_tasks(task_key=self._key, batch_size=self._batch_size, offset=self._offset):
                        await self._task_handler.start_task(task)

            else:
                self.stop()

    async def setup_next_task(self):
        ActorSystem.timer_ref.tell(AddActorMessage(actor=self.actor_ref, startTime=time.time() + self._job_call_duration))

    def stop_task(self):
        self._cancellation_task = True
        self.stop()

    def on_stop(self) -> None:
        ActorSystem.timer_ref.tell(StopTimerCommand(self.actor_ref))

    def _read_conf(self):
        config = AppSetting.APP_SETTINGS['scheduling_conf']
        self._job_call_duration = config["duration"]
        self._time_service = JobDateTimeService(start_time=config['daily_start_time'],
                                                end_time=config['daily_end_time'],
                                                timezone=config['timeZone'],
                                                time_format=config['time_format'])
        self._distributor = Distributor(daily_duration_hours=config["duration(hours)"],
                                        job_call_duration=self._job_call_duration)
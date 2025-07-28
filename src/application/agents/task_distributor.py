import asyncio
from typing import Any

from pykka import ThreadingActor

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages.start_job import StartJobCommand
from src.application.agents.task_runner import TaskOperator
from src.application.app_setting import AppSetting
from src.application.service import TaskService
from src.application.task.distributor import Distributor
from src.application.time.job_time_service import JobDateTimeService


class TaskDistributor(ThreadingActor):
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
            self.create_agents(msg.key)

    def create_agents(self, key):
        if not self._task_operators.get(key, None):
            task_operator = TaskOperator.start(key)
            self._task_operators.update({key: task_operator})

    def stop_agent(self, key):
        task_operator = self._task_operators.get(key, None)
        if task_operator:
            task_operator.stop()

    async def setup_next_task(self):
        ActorSystem.timer_ref.tell(AddActorMessage(actor=self.actor_ref, startTime=time.time() + self._job_call_duration))

    def _read_conf(self):
        config = AppSetting.APP_SETTINGS['scheduling_conf']
        self._job_call_duration = config["duration"]
        self._time_service = JobDateTimeService(start_time=config['daily_start_time'],
                                                end_time=config['daily_end_time'],
                                                timezone=config['timeZone'],
                                                time_format=config['time_format'])
        self._distributor = Distributor(daily_duration_hours=config["duration(hours)"],
                                        job_call_duration=self._job_call_duration)

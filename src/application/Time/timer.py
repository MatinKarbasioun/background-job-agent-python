from datetime import datetime
import logging
import asyncio
import pytz

import pykka
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job
from kink import inject

from src.application.agents.messages.time import TimeSignal
from src.application.app_setting import AppSetting


"""
Timer config:
The implemented timer using APScheduler as a timer engine for doing the periodical job
base on apscheduler library documentation:
user can use three types of job trigger:
1- date: use when you want to run the job just once at a certain point of time
2- interval: use when you want to run the job at fixed intervals of time
3- cron: use when you want to run the job periodically at certain time(s) of day

"""

logger = logging.getLogger(__name__)

@inject
class Timer(AsyncIOScheduler):
    def __init__(self, timezone: str = 'UTC', trigger: str = 'interval', **args):
        super().__init__(**args)
        self._trigger = trigger
        self._time_zone = timezone
        self._identification: dict[pykka.ActorRef, str] = {}
        self._last_triggered: dict[pykka.ActorRef, datetime] = {}
        self.__jobs: dict[pykka.ActorRef, Job] = {}

    def create(self, actor: pykka.ActorRef):
        self._identification[actor] = str(actor)
        self._last_triggered[actor] = datetime.now(tz=pytz.timezone(self._time_zone))

    def _delete(self, actor: pykka.ActorRef):
        if actor in self._identification:
            del self._identification[actor]

        if actor in self.__jobs:
            del self.__jobs[actor]

        if actor in self._last_triggered:
            del self._last_triggered[actor]

    def remove(self, actor: pykka.ActorRef):

        if actor in self.__jobs:
            self.__jobs[actor].remove()
        self._delete(actor)

    def call(self, actor: pykka.ActorRef, duration: int):
        now = datetime.now(tz=pytz.timezone(self._time_zone))
        self.__jobs[actor] = self.add_job(self._call,
                                          self._trigger,
                                          args=(actor,),
                                          seconds=duration,
                                          start_date=now,
                                          id=self._identification[actor],
                                          timezone=pytz.timezone(self._time_zone),
                                          replace_existing=True)

    def _call(self, actor_ref: pykka.ActorRef):
        try:
            actor_ref.tell(TimeSignal())

        except pykka.ActorDeadError as e:
            self.remove(actor_ref)
            logger.error(f"timer raised error for calling actor ref: {actor_ref} with error: {e}")


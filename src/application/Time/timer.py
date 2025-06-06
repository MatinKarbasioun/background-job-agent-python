from apscheduler.schedulers.background import BackgroundScheduler
from src.application.agent.message.time import TimeSignal
from apscheduler.job import Job
from datetime import datetime
from kink import inject
import pykka
import pytz

from src.application.app_setting import AppSetting


@inject
class Timer:
    def __init__(self, time_scheduler: BackgroundScheduler):
        super().__init__()
        app_setting_app = AppSetting.APP_SETTINGS['appConfig']
        self.__scheduler = time_scheduler
        self._time_zone = app_setting_app['timezone']
        self._identification: dict[pykka.ActorRef, str] = {}
        self._last_triggered: dict[pykka.ActorRef, datetime] = {}
        self.__jobs: dict[pykka.ActorRef, Job] = {}

    def create(self, actor: pykka.ActorRef):
        self._identification[actor] = str(actor)
        self._last_triggered[actor] = datetime.now(tz=pytz.timezone(self._time_zone))

    def __delete(self, actor: pykka.ActorRef):
        if actor in self._identification:
            del self._identification[actor]

        if actor in self.__jobs:
            del self.__jobs[actor]

        if actor in self._last_triggered:
            del self._last_triggered[actor]

    def stop(self, actor: pykka.ActorRef):

        if actor in self.__jobs:
            self.__jobs[actor].remove()
        self.__delete(actor)

    def shutdown(self):
        self.__scheduler.shutdown(wait=False)

    def call(self, actor: pykka.ActorRef, duration: int):
        now = datetime.now(tz=pytz.timezone(self._time_zone))
        self.__jobs[actor] = self.__scheduler.add_job(self.__call,
                                                      'interval',
                                                      args=[actor],
                                                      seconds=duration,
                                                      start_date=now,
                                                      id=self._identification[actor],
                                                      timezone=pytz.timezone(self._time_zone),
                                                      replace_existing=True)

    def __call(self, actor_ref: pykka.ActorRef):
        try:
            actor_ref.tell(TimeSignal())

        except Exception as e:
            self.stop(actor_ref)
            self.__delete(actor_ref)


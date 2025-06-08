import asyncio

from kink import di
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.application.Time import Timer
from src.application.agents.actor_sys import ActorSystem
from src.application.agents.task_distributor import TaskDistributor
from src.application.app_setting import AppSetting
from src.infrastructure.clients.client import TaskClient
from src.infrastructure.clients.task_client import ITaskClient
from src.infrastructure.repository.sqlalchemy.task import SqlAlchemyTaskRepository
from src.infrastructure.repository.task import ITaskRepository


class Bootstrap:
    def __init__(self):
        self._actor_sys: ActorSystem | None = None
        self._timer = self._setup_timer()
        self._db_engine =  self._setup_db()
        self._setup_db()
        self._setup_repo()
        self._setup_clients()

    @classmethod
    def _setup_timer(cls):
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(max_workers=5)
        }
        job_defaults = {
            'coalesce': AppSetting.APP_SETTINGS["timer_conf"]["coalesce"],
            'max_instances': AppSetting.APP_SETTINGS["timer_conf"]["max_instances"],
        }
        timezone = AppSetting.APP_SETTINGS["timer_conf"]["timezone"]
        return Timer(timezone=timezone, trigger='interval', executors=executors, job_defaults=job_defaults)

    @classmethod
    def _setup_db(cls):
        engine = create_async_engine(AppSetting.CREDENTIALS["db_conf"]["url"])
        di[AsyncEngine] = engine
        return engine

    @classmethod
    def _setup_repo(cls):
        di[ITaskRepository] = SqlAlchemyTaskRepository

    @classmethod
    def _setup_clients(cls):
        di[ITaskClient] = TaskClient

    def start(self):
        self._actor_sys = ActorSystem(initial_actor=TaskDistributor,
                                      event_loop=asyncio.get_event_loop(),
                                      timer=self._timer)
        self._actor_sys.start()
        self._timer.start()

    def stop(self):
        self._timer.shutdown(wait=True)
import asyncio
from kink import di
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.task_manager import TaskManager
from src.application.app_setting import AppSetting
from src.application.ports import ITaskClient
from src.application.time import Timer
from src.config.settings import get_settings
from src.domain.repositories import ITaskRepository
from src.infrastructure.adapters.client import TaskClient
from src.infrastructure.persistance.repository.sqlalchemy.task import SqlAlchemyTaskRepository


class Bootstrap:
    def __init__(self):
        settings = get_settings()
        self._actor_sys: ActorSystem | None = None
        self._timer = self._setup_timer()
        self._db_engine =  self._setup_db(settings.database_url)
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
    def _setup_db(cls, db_url: str):
        engine = create_async_engine(db_url)
        di[AsyncEngine] = engine
        return engine

    @classmethod
    def _setup_repo(cls):
        di[ITaskRepository] = SqlAlchemyTaskRepository

    @classmethod
    def _setup_clients(cls):
        di[ITaskClient] = TaskClient

    def start(self):
        self._actor_sys = ActorSystem(initial_actor=TaskManager, event_loop=asyncio.get_event_loop(), timer=self._timer)
        self._actor_sys()
        self._timer.start()

    def stop(self):
        self._timer.shutdown()
        self._actor_sys.stop()
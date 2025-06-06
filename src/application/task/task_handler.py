from asyncio import Queue, sleep

from kink import inject
from sqlalchemy.ext.asyncio import AsyncEngine

from src.application.task.distributor import Distributor
from src.domain import Task
from src.infrastructure.clients.task_client import ITaskClient
from src.infrastructure.db_manager.sql_alchemy.session import AsyncDatabaseSessionManager
from src.infrastructure.repository.task import ITaskRepository


@inject
class TaskHandler:
    def __init__(self, engine: AsyncEngine, task_repo: ITaskRepository, task_client: ITaskClient):
        self._task_repo = task_repo
        self._task_client = task_client
        self._distributor = Distributor()
        self._engine = engine
        self._cancellation = False

    async def get_open_tasks(self, task_key: str, batch_size: int = 1, offset: int = 0):

        async with AsyncDatabaseSessionManager(self._engine) as session:
            tasks = await self._task_repo.task_repo(session).get_open_tasks(task_key, offset, batch_size)

            for task in tasks:
                yield task

    async def start_task(self, task: Task):
        await self._task_client.start_task(task)

        async with AsyncDatabaseSessionManager() as session:
            await self._task_repo.task_repo(session).update_task(task)

    async def task_count(self, key):
        async with AsyncDatabaseSessionManager as session:
            return await self._task_repo.task_repo(session).task_count(key)

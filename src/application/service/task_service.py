from kink import inject
from sqlalchemy.ext.asyncio import AsyncEngine

from src.application.ports import ITaskClient
from src.domain import Task

from src.domain.repositories import ITaskRepository
from src.infrastructure.persistance import AsyncDatabaseSessionManager


@inject
class TaskService:
    def __init__(self, engine: AsyncEngine, task_repo: ITaskRepository, task_client: ITaskClient):
        self._task_repo = task_repo
        self._task_client = task_client
        self._engine = engine
        self._cancellation = False

    async def is_exist(self, job_id) -> bool:
        async with AsyncDatabaseSessionManager(self._engine) as session:
            return await self._task_repo.task_repo(session).is_exist(job_id)

    async def get_open_tasks(self, task_key: str, batch_size: int = 1, offset: int = 0):

        async with AsyncDatabaseSessionManager(self._engine) as session:
            tasks = await self._task_repo.task_repo(session).get_open_tasks(task_key, offset, batch_size)

            for task in tasks:
                yield task

    async def start_task(self, task: Task):
        await self._task_client.start_task(task)

        async with AsyncDatabaseSessionManager(self._engine) as session:
            await self._task_repo.task_repo(session).update_task(task)

    async def task_count(self, key):
        async with AsyncDatabaseSessionManager(self._engine) as session:
            return await self._task_repo.task_repo(session).task_count(key)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, exists
from sqlalchemy import func

from src.domain import Task
from src.infrastructure.models.task_model import TaskModel
from src.infrastructure.repository.extensions.task import toTask
from src.infrastructure.repository.task import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def is_exist(self, job_id: str) -> bool:
        stmt = select(exists(select(TaskModel).where(TaskModel.job_id==job_id)))
        result = await self._session.execute(stmt)
        return result.scalar()

    async def task_count(self, job_id: str) -> int:
        return await self._session.scalar(func.count(TaskModel.job_id == job_id))

    async def get_open_tasks(self, job_id: str, offset: int, batch_size: int) -> list[Task]:
        stmt = select(TaskModel).where(TaskModel.job_id == job_id).limit(batch_size).offset(offset)
        result = await self._session.execute(stmt)
        tasks = result.scalars()
        return [task @ toTask for task in tasks]

    async def update_task(self, task: Task):
        stmt = update(TaskModel).where(TaskModel.task_id == task.task_id).values(star_date=task.start_date,
                                                                                 error=task.error)
        await self._session.execute(stmt)
        await self._session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy import func

from src.domain import Task
from src.infrastructure.models.task_model import TaskModel
from src.infrastructure.repository.extensions.task import toTask
from src.infrastructure.repository.task import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def task_count(self, task_key: str) -> int:
        return await self._session.scalar(func.count(TaskModel.batch_key == task_key))

    async def get_open_tasks(self, batch_key: str, offset: int, batch_size: int) -> list[Task]:
        stmt = select(TaskModel).where(TaskModel.batch_key == batch_key).limit(batch_size).offset(offset)
        result = await self._session.execute(stmt)
        tasks = result.scalars()
        return [task @ toTask for task in tasks]

    async def update_task(self, task: Task):
        stmt = update(TaskModel).where(TaskModel.task_id == task.task_id).values(star_date=task.start_date,
                                                                                 error=task.error)
        await self._session.execute(stmt)
        await self._session.commit()

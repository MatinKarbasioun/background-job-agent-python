from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, exists
from sqlalchemy import func
from sqlalchemy import and_

from src.domain import Task
from src.infrastructure.persistance.models import SqlServerTaskModel
from src.infrastructure.persistance.repository.extensions.task import ToTask
from src.domain.repositories.task import ITaskRepository


class SqlAlchemyTaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def is_exist(self, job_id: str) -> bool:
        stmt = select(exists(select(SqlServerTaskModel).where(and_(SqlServerTaskModel.job_id==job_id,
                                                                   SqlServerTaskModel.start_date == None,
                                                                   SqlServerTaskModel.error==None))))
        result = await self._session.execute(stmt)
        return result.scalar()

    async def task_count(self, job_id: str) -> int:
        return await self._session.scalar(func.count(and_(SqlServerTaskModel.job_id==job_id,
                                                          SqlServerTaskModel.start_date == None,
                                                          SqlServerTaskModel.error==None)))

    async def get_open_tasks(self, job_id: str, offset: int, batch_size: int) -> list[Task]:
        stmt = select(SqlServerTaskModel).where(and_(SqlServerTaskModel.job_id==job_id,
                                                     SqlServerTaskModel.start_date == None,
                                                     SqlServerTaskModel.error==None)).limit(batch_size).offset(offset)
        result = await self._session.execute(stmt)
        tasks = result.scalars()
        return [task @ ToTask() for task in tasks]

    async def update_task(self, task: Task):
        stmt = update(SqlServerTaskModel).where(SqlServerTaskModel.task_id == task.task_id).values(
            star_date=task.start_date,
            error=task.error
        )
        await self._session.execute(stmt)
        await self._session.commit()

    @classmethod
    def task_repo(cls, session) -> 'ITaskRepository':
        return cls(session)

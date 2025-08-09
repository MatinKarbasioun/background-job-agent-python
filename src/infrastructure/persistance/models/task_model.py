from sqlalchemy import Column, BigInteger, DATETIME, String

from src.infrastructure.persistance.db_manager.sql_alchemy.base import BaseModel


class SqlServerTaskModel(BaseModel):
    __tablename__ = "task"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(String, nullable=False, unique=True)
    task_id = Column(BigInteger, nullable=False)
    start_date = Column(DATETIME, nullable=True)
    error = Column(String, nullable=True)
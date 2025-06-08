from pydantic import BaseModel, validator, field_validator
from fastapi.exceptions import HTTPException

from src.application.task.task_handler import TaskHandler


class JobRequest(BaseModel):
    job_id: str


    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v):
        if not TaskHandler().is_exist(v.job_id):
            raise HTTPException(status_code=404)

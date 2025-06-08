from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: int
    is_success: bool
    error: str | None = None

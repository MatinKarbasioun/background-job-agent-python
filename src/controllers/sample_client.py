from fastapi import APIRouter

from src.application.schemas.tasks.task import TaskResponse

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.put("/{task_id}")
def start_task(task_id: int) -> TaskResponse:
    try:
        return TaskResponse(is_success=True, task_id=task_id)

    except Exception as e:
        return TaskResponse(is_success=False, task_id=task_id, error=str(e))
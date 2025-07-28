from fastapi.exceptions import HTTPException
from typing import Annotated

from fastapi import BackgroundTasks, APIRouter, Depends

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StartJobCommand, StopJobCommand
from src.application.service import TaskService
from src.controllers.dependencies import Dependencies

job_router = APIRouter(prefix='/jobs', tags=["jobs"])


@job_router.post("", status_code=200)
async def create_job(job: JobRequest, background_tasks: BackgroundTasks, task_service: Annotated[TaskService, Depends(Dependencies.task_handler)]) -> AddJobSuccessfully:

    if await task_handler.is_exist(job.job_id):
        background_tasks.add_task(ActorSystem.tell, StartJobCommand(job.job_id))
        return AddJobSuccessfully(msg=f"job id {job.job_id} started successfully")

    else:
        raise HTTPException(status_code=404, detail=f"job id {job.job_id} does not exist")


@job_router.put("", status_code=200)
async def stop_job(job: JobRequest, background_tasks: BackgroundTasks) -> StopJobSuccessfully:
    background_tasks.add_task(ActorSystem.tell, StopJobCommand(job.job_id))
    return StopJobSuccessfully(msg=f"job id {job.job_id} stopped successfully")
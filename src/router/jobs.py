from typing import Annotated

from fastapi import BackgroundTasks, APIRouter, Depends, Response, status

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StartJobCommand, StopJobCommand
from src.application.task.task_handler import TaskHandler
from src.router.dependencies.dependencies import Dependencies
from src.schemas.jobs import *


job_router = APIRouter(prefix='/jobs', tags=["jobs"])


@job_router.post("", status_code=200)
async def create_job(job: JobRequest, background_tasks: BackgroundTasks, task_handler: Annotated[TaskHandler, Depends(Dependencies.task_handler)]) -> AddJobSuccessfully:
    if task_handler.is_exist(job.job_id):
        background_tasks.add_task(ActorSystem.tell, StartJobCommand(job.job_id))
        return AddJobSuccessfully(msg=f"job id {job.job_id} started successfully")

    else:
        return Response(content={"msg": "the job id not found"}, status_code=status.HTTP_404_NOT_FOUND)

@job_router.put("", status_code=200)
async def stop_job(job: JobRequest, background_tasks: BackgroundTasks) -> StopJobSuccessfully:
    background_tasks.add_task(ActorSystem.tell, StopJobCommand(job.job_id))
    return StopJobSuccessfully(msg=f"job id {job.job_id} stopped successfully")
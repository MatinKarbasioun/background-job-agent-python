from fastapi import BackgroundTasks, APIRouter

from src.application.agents.actor_sys import ActorSystem
from src.application.agents.messages import StartJobCommand, StopJobCommand
from src.schemas.jobs import *


job_router = APIRouter(prefix='/jobs', tags=["jobs"])


@job_router.post("", status_code=200)
async def create_job(job: JobRequest, background_tasks: BackgroundTasks) -> AddJobSuccessfully:
    background_tasks.add_task(ActorSystem.tell, StartJobCommand(job.job_id))
    return AddJobSuccessfully(msg=f"job id {job.job_id} started successfully")

@job_router.put("", status_code=200)
async def stop_job(job: JobRequest, background_tasks: BackgroundTasks) -> StopJobSuccessfully:
    background_tasks.add_task(ActorSystem.tell, StopJobCommand(job.job_id))
    return StopJobSuccessfully(msg=f"job id {job.job_id} stopped successfully")
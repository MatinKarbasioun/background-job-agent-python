import aiohttp

from src.application.ports.task_client import ITaskClient
from src.domain import Task


class TaskClient(ITaskClient):

    async def start_task(self, task_id: int) -> Task:
        async with aiohttp.ClientSession() as session:
            async with session.put("http://localhost:8080/tasks/{}".format(task_id)) as resp:
                if resp.status == 200:
                    return Task(is_success=True, task_id=task_id)

                else:
                    return Task(is_success=False, task_id=task_id, error=await resp.text('utf-8'))

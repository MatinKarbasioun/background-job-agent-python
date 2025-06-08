import aiohttp

from src.infrastructure.clients.task_client import ITaskClient
from src.infrastructure.clients.task_response import TaskResponse


class TaskClient(ITaskClient):

    async def start_task(self, task_id: int) -> TaskResponse:
        async with aiohttp.ClientSession() as session:
            async with session.put("http://localhost:8080/tasks/{}".format(task_id)) as resp:
                if resp.status == 200:
                    return TaskResponse(is_success=True, task_id=task_id)

                else:
                    return TaskResponse(is_success=False, task_id=task_id, error=await resp.text('utf-8'))

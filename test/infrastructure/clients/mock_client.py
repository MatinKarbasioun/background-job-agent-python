from src.application.ports import ITaskClient
from src.application.schemas import TaskResponse


class MockTaskClient(ITaskClient):
    def __init__(self, success: bool = True):
        self._success = success

    async def start_task(self, task_id: int) -> TaskResponse:
        return TaskResponse(is_success=self._success, task_id=task_id, error=None if self._success else 'some error')

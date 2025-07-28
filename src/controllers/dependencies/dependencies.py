from src.application.service.task_service import TaskService


class Dependencies:

    def __init__(self):
        pass

    @classmethod
    async def task_service(cls):
        return TaskService()

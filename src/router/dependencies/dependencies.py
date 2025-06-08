from src.application.task.task_handler import TaskHandler


class Dependencies:

    def __init__(self):
        pass

    @classmethod
    async def task_handler(cls):
        return TaskHandler()

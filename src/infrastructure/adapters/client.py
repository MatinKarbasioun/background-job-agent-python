import datetime

import aiohttp
import pytz

from src.application.app_setting import AppSetting
from src.application.ports.task_client import ITaskClient
from src.domain import Task
from src.domain.value_objects import TaskStatus


class TaskClient(ITaskClient):

    async def start_task(self, task: Task):
        async with aiohttp.ClientSession() as session:
            async with session.put("http://localhost:8080/tasks/{}".format(task.task_id)) as resp:
                if resp.status == 200:
                    task.status = TaskStatus.COMPLETED
                    task.start_date = datetime.datetime.now(pytz.timezone(AppSetting.APP_SETTINGS['timezone']))

                else:
                    task.status = TaskStatus.FAILED
                    task.error = await resp.text('utf-8')

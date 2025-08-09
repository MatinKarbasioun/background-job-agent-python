class TaskDistributor:
    def __init__(self, daily_duration_hours: float, job_call_duration: int):
        self._daily_duration_hours = daily_duration_hours
        self._job_call_duration = job_call_duration

    def distribute(self, tasks_count: int):
        duration_sec = self._daily_duration_hours * 3600
        tasks_per_call = (tasks_count // duration_sec) * self._job_call_duration
        return tasks_per_call if tasks_per_call >= 1 else 1

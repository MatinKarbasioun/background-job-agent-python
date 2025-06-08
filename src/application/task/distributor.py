class Distributor:
    def __init__(self, duration: int):
        self._duration = duration

    def calculate(self, tasks_count: int):
        duration_sec = self._duration * 3600
        return tasks_count // duration_sec if tasks_count != 0 else 1

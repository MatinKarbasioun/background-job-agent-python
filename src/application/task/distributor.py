class Distributor:
    def __init__(self, config: dict):
        self._config = config

    def calculate(self, tasks_count: int):
        duration = self._config['duration']
        duration_sec = duration * 3600
        return tasks_count // duration_sec if tasks_count != 0 else 1

class Dependency:
    def __init__(self):
        self._repo = None

    @classmethod
    def job_repo(cls):
        return self._repo

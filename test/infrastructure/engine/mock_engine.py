from sqlalchemy.ext.asyncio import AsyncEngine


class MockEngine(AsyncEngine):
    def __init__(self):
        super().__init__()
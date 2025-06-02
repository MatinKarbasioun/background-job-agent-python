from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class DatabaseManager:
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._connection = None
        
    def connect(self) -> AsyncEngine:
        self._connection =  create_async_engine(url=self._db_url, echo=False)
        return self._connection
    
from contextlib import asynccontextmanager
from .router import *

from fastapi import FastAPI

from src.app.bootstrap import Bootstrap
from src.application.app_setting import AppSetting


@asynccontextmanager
async def lifespan(app: FastAPI):
    AppSetting()
    Bootstrap().start()

    yield
    Bootstrap().stop()


app = FastAPI(lifespan=lifespan, docs_url='/swagger')
app.include_router(app_router)
app.include_router(job_router)
app.include_router(task_router)


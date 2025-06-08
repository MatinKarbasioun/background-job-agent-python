from contextlib import asynccontextmanager

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

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


app = FastAPI(lifespan=lifespan, title='background-job-runner-agent', version='1.0.0', debug=True, docs_url='/swagger')
app.include_router(app_router)
app.include_router(job_router)
app.include_router(task_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"msg": "Bad Request", "detail": exc.errors(), "body": exc.body}),
    )

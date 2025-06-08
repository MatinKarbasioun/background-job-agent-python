from fastapi import APIRouter

from src.schemas.app import ApplicationResponse

app_router = APIRouter(prefix="", tags=["app"])

@app_router.get("/", status_code=200)
def application() -> ApplicationResponse:
    return ApplicationResponse()
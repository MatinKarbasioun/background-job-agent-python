from pydantic import BaseModel


class ApplicationResponse(BaseModel):
    msg: str = "application is up and running"
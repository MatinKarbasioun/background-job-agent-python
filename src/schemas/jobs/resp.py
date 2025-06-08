from pydantic import BaseModel


class AddJobSuccessfully(BaseModel):
    msg: str

class StopJobSuccessfully(BaseModel):
    msg: str

class JobNotFound(BaseModel):
    msg: str
from contextlib import asynccontextmanager


from fastapi import FastAPI, BackgroundTasks



@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


app = FastAPI(lifespan=lifespan)


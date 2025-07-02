from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.v1.utils.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

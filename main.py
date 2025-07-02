from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.v1.utils.db import init_db
from app.v1.router import user_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router.router)

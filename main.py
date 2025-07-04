from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
from app.v1.utils.db import init_db
from app.v1.router.user_router import user_router

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server started at {datetime.now()} ")
    await init_db()
    yield
    print(f"Server has been stop at {datetime.now()} ")


app = FastAPI(lifespan=life_span)
app.include_router(user_router, prefix="/api/users")

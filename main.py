from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
from app.v1.router.admin_router import admin_router
from app.v1.utils.db import init_db
from app.v1.router.user_router import user_router
from app.v1.router.todo_router import todo_router

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server started at {datetime.now()} ")
    await init_db()
    yield
    print(f"Server has been stop at {datetime.now()} ")


app = FastAPI(
    title="TODO App",
    description="A REST API for a todo list",
    version="v1"
)
# Users routes
app.include_router(user_router, prefix="/api/users")

# Todos routes
app.include_router(todo_router, prefix="/api")

# Admins routes
app.include_router(admin_router, prefix="/api/admin")

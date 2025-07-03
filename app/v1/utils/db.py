from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from app.v1.utils.settings import Config
from app.v1.model.user_model import User
from app.v1.model.todo_model import Todo


# Asynchronous database
engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from app.v1.utils.settings import Config
from sqlalchemy.orm import sessionmaker
from app.v1.model.user_model import User
from app.v1.model.todo_model import Todo

# Asynchronous database
async_engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session =  sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session
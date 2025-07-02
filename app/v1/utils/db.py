from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.v1.utils.settings import Settings

# Asynchronous database
settings = Settings()
assert settings.database_url, "DATABASE_URL is not set in environment variables"

if not settings.database_url.startswith("postgresql+asyncpg://"):
    DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    DATABASE_URL = settings.database_url

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Initialize database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
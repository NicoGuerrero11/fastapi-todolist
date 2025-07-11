from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.v1.model.todo_model import Todo
from app.v1.model.user_model import User

from app.v1.schema.user_schema import UserRead


class AdminService:
    async def get_all_todos(self, session: AsyncSession) -> list[Todo]:
        statement = select(Todo).order_by(desc(Todo.created_at))
        result = await session.exec(statement)
        if result is None:
            return []
        return result.all()

    async def get_all_users(self, session: AsyncSession) -> list[UserRead]:
        statement = select(User).order_by(desc(User.created_at))
        result = await session.exec(statement)
        if result is None:
            return []
        return result.all()
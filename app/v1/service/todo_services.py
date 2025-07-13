from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.schema.todos_schema import TodoCreate, TodoUpdate
from sqlmodel import select
from app.v1.model.todo_model import Todo
import uuid
from app.v1.scripts.errors import TaskNotFound
from app.v1.scripts.token_validation import validate_owner

class TodoService:

    # User
    async def get_user_todos(self, user_uid:uuid.UUID ,session:AsyncSession, user_details) -> list[Todo]:
        statement = select(Todo).where(Todo.user_id == user_uid)
        result = await session.exec(statement)
        if result is None:
            return []
        validate_owner(str(user_uid), user_details["user"]["user_uid"])
        return result.all()


    async def get_todo(self, todo_id:uuid.UUID, session:AsyncSession, user_details:dict) -> Todo:
        statement = select(Todo).where(Todo.id == todo_id)
        result = await session.exec(statement)
        todo = result.first()
        if todo is None:
            raise TaskNotFound()
        validate_owner(str(todo.user_id), user_details["user"]["user_uid"])
        return todo


    async def create_todo(self, todo_data:TodoCreate, session:AsyncSession, user_details:dict) -> Todo:
        todo_data_dict = todo_data.model_dump()
        todo_data_dict["user_id"] = user_details["user"]["user_uid"]
        new_todo = Todo(**todo_data_dict)
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo


    async def update_todo(self, todo_id:uuid.UUID, update_data:TodoUpdate,session:AsyncSession, user_details: dict) -> Todo:
        todo_to_update = await self.get_todo(todo_id, session, user_details)
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for k, v in update_data_dict.items():
            setattr(todo_to_update, k, v)
        await session.commit()
        await session.refresh(todo_to_update)
        return todo_to_update



    async def delete_todo(self, todo_id:uuid.UUID, session:AsyncSession, user_details: dict) -> bool:
        todo_to_delete = await self.get_todo(todo_id, session, user_details)
        await session.delete(todo_to_delete)
        await session.commit()
        return True


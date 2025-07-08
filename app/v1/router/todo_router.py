from fastapi import APIRouter, status, Depends, HTTPException
from app.v1.schema.todos_schema import TodoRead, TodoUpdate, TodoCreate
from app.v1.service.todo_services import TodoService
from app.v1.utils.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID
from app.v1.dependencies.auth import TokenBearer

todo_router = APIRouter()
ts = TodoService()
security = TokenBearer()

# Admins
@todo_router.get("/admin/todos", response_model=List[TodoRead])
async def get_todos(session: AsyncSession = Depends(get_session), user_details=Depends(security)):
    todos = await ts.get_all_todos(session)
    return todos

# Users
@todo_router.get("/users/todos/{user_uid}", response_model=List[TodoRead])
async def get_user_todos(user_uid: UUID, session: AsyncSession = Depends(get_session), user_details=Depends(security)):
    todo = await ts.get_user_todos(user_uid ,session )
    return todo

@todo_router.get("/todos/{todo_id}", response_model=List[TodoRead])
async def get_single_todo(todo_id: UUID, session: AsyncSession = Depends(get_session),user_details=Depends(security)):
    todo = await ts.get_todo(todo_id, session)
    return todo

@todo_router.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoRead)
async def create_todo(todo_data: TodoCreate, session: AsyncSession = Depends(get_session),user_details=Depends(security)):
    new_todo = await ts.create_todo(todo_data, session, user_details)
    return new_todo

@todo_router.patch("/todos/{todo_id}", response_model=TodoRead)
async def update_todo(todo_id: UUID, update_data:TodoUpdate, session: AsyncSession = Depends(get_session),user_details=Depends(security)):
    upd_todo = await ts.update_todo(todo_id, update_data, session)

    if upd_todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return upd_todo

@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, session: AsyncSession = Depends(get_session),user_details=Depends(security)):
    todo_delete = await ts.delete_todo(todo_id, session)

    if todo_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo_delete
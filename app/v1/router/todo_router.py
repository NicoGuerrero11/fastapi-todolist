from fastapi import APIRouter, status, Depends, HTTPException
from app.v1.schema.todos_schema import TodoRead, TodoUpdate, TodoCreate
from app.v1.service.todo_services import TodoService
from app.v1.utils.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID
from app.v1.dependencies.auth import AccessTokenBearer
from app.v1.dependencies.roles import RoleCheck

todo_router = APIRouter()
ts = TodoService()
access_token = AccessTokenBearer()
role_check = RoleCheck(['user'])

@todo_router.get("/users/todos/{user_uid}", response_model=List[TodoRead],
                 dependencies=[Depends(RoleCheck(['user', 'admin']))])
async def get_user_todos(user_uid: UUID, session: AsyncSession = Depends(get_session), user_details=Depends(access_token)):
    todo = await ts.get_user_todos(user_uid ,session, user_details)
    return todo

@todo_router.get("/todos/{todo_id}", response_model=TodoRead, dependencies=[Depends(role_check)])
async def get_single_todo(todo_id: UUID, session: AsyncSession = Depends(get_session),user_details=Depends(access_token)):
    todo = await ts.get_todo(todo_id, session, user_details )
    return todo

@todo_router.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoRead, dependencies=[Depends(role_check)])
async def create_todo(todo_data: TodoCreate, session: AsyncSession = Depends(get_session),user_details=Depends(access_token)):
    new_todo = await ts.create_todo(todo_data, session, user_details)
    return new_todo

@todo_router.patch("/todos/{todo_id}", response_model=TodoRead, dependencies=[Depends(role_check)])
async def update_todo(todo_id: UUID, update_data:TodoUpdate, session: AsyncSession = Depends(get_session),user_details=Depends(access_token)):
    upd_todo = await ts.update_todo(todo_id, update_data, session, user_details)
    if upd_todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return upd_todo

@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_check)])
async def delete_todo(todo_id: UUID, session: AsyncSession = Depends(get_session),user_details=Depends(access_token)):
    todo_delete = await ts.delete_todo(todo_id, session, user_details)

    if todo_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo_delete
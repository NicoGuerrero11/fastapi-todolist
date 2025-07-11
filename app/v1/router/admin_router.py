from fastapi import APIRouter,Depends
from app.v1.service.admin_services import AdminService
from app.v1.dependencies.roles import RoleCheck
from app.v1.schema.todos_schema import TodoRead
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.utils.db import get_session
from app.v1.schema.user_schema import UserRead
from app.v1.dependencies.auth import AccessTokenBearer


admin_router = APIRouter()
ts = AdminService()
access_token = AccessTokenBearer()
role_check = RoleCheck(['admin'])

# get all todos
@admin_router.get("/todos", response_model=List[TodoRead], dependencies=[Depends(role_check)])
async def get_todos(session: AsyncSession = Depends(get_session)):
    todos = await ts.get_all_todos(session)
    return todos

#get all users
@admin_router.get("/users", response_model=List[UserRead], dependencies=[Depends(role_check)])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await ts.get_all_users(session)
    return users
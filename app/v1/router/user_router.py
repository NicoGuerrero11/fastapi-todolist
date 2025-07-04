from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.utils.db import get_session
from app.v1.service.user_service import UserService
from app.v1.schema.user_schema import UserCreate, UserUpdate, UserLogin, UserRead

user_router = APIRouter()
Us = UserService()

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_create = await Us.register_user(user_data, session)
    return user_create
@user_router.post("/login", response_model=UserRead)
async def login(credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    return await Us.login_user(credentials, session)



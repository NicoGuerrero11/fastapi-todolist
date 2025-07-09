from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.utils.db import get_session
from app.v1.service.user_service import UserService
from app.v1.schema.user_schema import UserCreate, UserLogin, UserRead, TokenResponse
from app.v1.dependencies.auth import RefreshTokenBearer, AccessTokenBearer


user_router = APIRouter()
Us = UserService()
refresh_token = RefreshTokenBearer()

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_create = await Us.register_user(user_data, session)
    return user_create
@user_router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    return await Us.login_user(credentials, session)

@user_router.get("/refresh", response_model=TokenResponse)
async def refresh(user_details: dict = Depends(refresh_token), session: AsyncSession = Depends(get_session)):
    return await Us.refresh_user_token(user_details, session)

@user_router.get("/logout")
async def revoke_token(user_details: dict = Depends(AccessTokenBearer())):
    return await Us.revoke_token(user_details)
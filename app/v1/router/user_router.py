from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.v1.utils.db import get_session
from app.v1.service import user_service
from app.v1.schema.user_schema import UserRegister, User

router = APIRouter()

@router.post("/user/", response_model=User)
async def create_user(
    user: UserRegister,
    session: Session = Depends(get_session)
):
    return await user_service.create_user(user, session)
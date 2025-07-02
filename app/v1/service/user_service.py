from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema
from sqlmodel import select


from app.v1.schema.user_schema import UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(user: UserRegister, session: AsyncSession):
    statement = select(UserModel).where(
        (UserModel.email == user.email) | (UserModel.username == user.username)
    )
    result = await session.exec(statement)
    existing_user = result.first()

    if existing_user:
        msg = "Email already registered"
        if existing_user.username == user.username:
            msg = "Username already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )

    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return user_schema.User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )
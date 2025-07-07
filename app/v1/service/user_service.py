from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.v1.model.user_model import User
from app.v1.schema.user_schema import UserCreate, UserLogin,UserRead, TokenResponse
from app.v1.scripts.token import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    async def register_user(self, user_data: UserCreate, session: AsyncSession) -> UserRead:
        # Check if the user already exists
        statement  = select(User).where(User.email == user_data.email)
        result = await session.exec(statement )
        existing_user = result.first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Hash the password and create the user
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserRead.model_validate(new_user)

    async def login_user(self, credentials: UserLogin, session: AsyncSession) -> TokenResponse:
        statement  = select(User).where(User.email == credentials.email)
        result = await session.exec(statement)
        user = result.first()
        if not user or not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        token = create_access_token({"sub": str(user.uid)})
        return TokenResponse(access_token=token)

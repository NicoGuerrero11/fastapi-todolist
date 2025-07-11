from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status
from app.v1.utils.redis import add_jti_to_blocklist
from app.v1.model.user_model import User
from app.v1.schema.user_schema import UserCreate, UserLogin,UserRead, TokenResponse
from app.v1.scripts.token import create_access_token, decode_token
from app.v1.scripts.hash_password import hash_password, verify_password
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def register_user(self, user_data: UserCreate, session: AsyncSession) -> UserRead:
        # Check if the user already exists
        statement  = select(User).where(User.email == user_data.email)
        result = await session.exec(statement )
        existing_user = result.first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Hash the password and create the user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            role="user"
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserRead.model_validate(new_user)

    async def login_user(self, credentials: UserLogin, session: AsyncSession) -> TokenResponse:
        statement  = select(User).where(User.email == credentials.email)
        result = await session.exec(statement)
        user = result.first()
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        access_token = create_access_token(
            user_data={
                "email": user.email,
                "user_uid": str(user.uid)
            }
        )
        refresh_token = create_access_token(
            user_data={
                "email": user.email,
                "user_uid": str(user.uid)
            },
            refresh=True,
            expiry=timedelta(days=2)
        )

        return TokenResponse(
            user_uid=str(user.uid),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    async def refresh_user_token(self, user_details: dict, session: AsyncSession) -> JSONResponse:
        expires_in = user_details['exp']

        if datetime.fromtimestamp(expires_in) > datetime.now():
            new_access_token = create_access_token(
                user_data=user_details['user']
            )
            return JSONResponse(content={"new_access_token": new_access_token})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expire token")

    async def revoke_token(self, user_details: dict) -> JSONResponse:
        jti = user_details['jti']
        await add_jti_to_blocklist(jti)

        return JSONResponse(
            content={
                "message": "Successfully logged out",
            },
            status_code = status.HTTP_200_OK
        )


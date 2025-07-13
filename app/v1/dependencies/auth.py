from fastapi import Request, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from app.v1.scripts.token import decode_token
from fastapi.exceptions import HTTPException
from app.v1.utils.redis import token_in_blocklist
from app.v1.utils.db import get_session
from app.v1.service.user_service import UserService
from app.v1.scripts.errors import InvalidToken, RevokedToken,AccessTokenRequired,RefreshTokenRequired

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        # creds.schema -> bearer
        # creds.credentials -> token
        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()
        if await token_in_blocklist(token_data['jti']):
            raise RevokedToken()

        self.verify_token_data(token_data)

        return token_data


    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self,token_data):
        raise NotImplementedError("Please override this method in child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh_token"):
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh_token"):
            raise RefreshTokenRequired()

async def get_current_user(token_details: dict = Depends(AccessTokenBearer()),
                     session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user

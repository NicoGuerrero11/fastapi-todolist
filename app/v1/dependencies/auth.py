from fastapi import Request, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from app.v1.scripts.token import decode_token
from fastapi.exceptions import HTTPException
from app.v1.utils.redis import token_in_blocklist

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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token."
                       "Resolution: Please get new Token."
            )
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="error: This token is invalid or has been revoked,"
                       "Resolution: Please get new Token."
            )

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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token."
            )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token."
            )
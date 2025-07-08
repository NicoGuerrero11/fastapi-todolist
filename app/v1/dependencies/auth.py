from fastapi import Request, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from app.v1.scripts.token import decode_token
from fastapi.exceptions import HTTPException

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error = auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        # creds.schema -> bearer
        # creds.credentials -> token
        token = creds.credentials

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token."
            )
        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token."
            )

        if token_data.get("refresh_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token."
            )
        return token_data


    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return True if token_data is not None else False


import logging
import uuid

import jwt
from datetime import timedelta, datetime, timezone
from app.v1.utils.settings import Config

TOKEN_EXPIRATION = timedelta(hours=1)

def create_access_token(user_data: dict, expiry: timedelta = TOKEN_EXPIRATION, refresh: bool=False ):
    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc) + (expiry if expiry is not None else TOKEN_EXPIRATION),
        'jti': str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token:str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
import uuid

import jwt
from datetime import timedelta, datetime
from app.v1.utils.settings import Config

TOKEN_EXPIRATION = 3600

def create_access_token(user_data: dict, expiry:timedelta = None, refresh: bool=False ):
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry is not None else timedelta(seconds=TOKEN_EXPIRATION)),
        'jti': str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    return token
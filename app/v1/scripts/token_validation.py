import uuid
from app.v1.scripts.errors import InsufficientPermission


def validate_owner(user_uid: str, token_id: uuid.UUID) -> bool:
    if user_uid != token_id:
        raise InsufficientPermission()
    return True
import uuid
from fastapi import HTTPException, status


def validate_owner(user_uid: str, token_id: uuid.UUID) -> bool:
    if user_uid != token_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )
    return True
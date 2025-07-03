from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserSchema):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserSchema):
    uid: UUID

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
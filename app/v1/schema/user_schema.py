from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class UserSchema(BaseModel):
    username: str = Field(max_length=64)
    email: EmailStr = Field(max_length=64)

class UserCreate(UserSchema):
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=6)

class UserRead(UserSchema):
    uid: UUID

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    user_uid: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
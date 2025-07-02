from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["myemail@cosasdedevs.com"])
    username: str = Field(..., min_length=3, max_length=50, examples=["MyTypicalUsername"])


class User(UserBase):
    id: int = Field(..., examples=[5])


class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=64, examples=["strongpass"])
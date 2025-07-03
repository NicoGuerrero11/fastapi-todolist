from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title: str
    is_done: bool = False

# Post
class TodoCreate(TodoBase):
    pass

#Patch
class TodoUpdate(TodoBase):
    title: Optional[str] = None
    is_done: Optional[bool] = None

#Get
class TodoRead(TodoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True

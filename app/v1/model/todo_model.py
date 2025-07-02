from datetime import datetime
from sqlmodel import Field, SQLModel

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    is_done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
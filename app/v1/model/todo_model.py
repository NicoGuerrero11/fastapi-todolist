from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid

class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    is_done: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user_id: uuid.UUID = Field(foreign_key="users.uid")

    def __repr__(self) -> str:
        return f"<TODO {self.title}>"
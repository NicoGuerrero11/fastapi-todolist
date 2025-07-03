from datetime import datetime
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class Todo(SQLModel, table=True):
    __tablename__ = "todos"
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    title: str
    is_done: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_id: uuid.UUID = Field(foreign_key="users.uid")

    def __repr__(self) -> str:
        return f"<TODO {self.title}>"
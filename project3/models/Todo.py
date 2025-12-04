from sqlmodel import SQLModel, Field
from datetime import datetime
from models.TodoBase import TodoBase

class Todo(TodoBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
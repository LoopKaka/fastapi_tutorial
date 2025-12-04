from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    title: str = Field(min_length=2, max_length=10, nullable=False)
    description: str = Field(min_length=5, max_length=50, nullable=True)
    priority: int = Field(le=5, ge=1, default=1)
    is_completed: bool = Field(default=False)
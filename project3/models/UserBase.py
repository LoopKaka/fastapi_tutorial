from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    password: str = Field(max_length=250, nullable=False)
    name: str = Field(nullable=False, min_length=3, max_length=20)

from sqlmodel import Field
from models.UserBase import UserBase
from datetime import datetime

class User(UserBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    
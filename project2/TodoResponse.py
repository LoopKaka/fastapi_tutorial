from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: int
    title: str
    descriptions: str
    is_completed: bool
    priority: int
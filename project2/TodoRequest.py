from typing import Optional
from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    id: Optional[int] = Field(ge=1, description="During Todo creation ID is not required", default=None)
    title: str = Field(min_length=2, max_length=15)
    descriptions: str = Field(min_length=2, max_length=50)
    is_completed: Optional[bool] = Field(default=False)
    priority: int = Field(le=5, ge=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Todo Title",
                "descriptions": "Todo Description",
                "is_completed": False,
                "priority": 4
            }
        }
    }

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkOrderStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class WorkOrderCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=1000)

    @field_validator("title", "description")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty or whitespace")
        return value


class WorkOrderStatusUpdate(BaseModel):
    status: WorkOrderStatus


class WorkOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: WorkOrderStatus
    created_at: datetime
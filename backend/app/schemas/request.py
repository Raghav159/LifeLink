from pydantic import BaseModel, Field
from typing import Optional
import uuid
from enum import Enum


class UrgencyLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RequestBase(BaseModel):
    blood_group_required: str = Field(..., example="O+")
    latitude: float
    longitude: float
    urgency_level: UrgencyLevel
    quantity: int = Field(..., gt=0)


class RequestCreate(RequestBase):
    pass


class RequestResponse(RequestBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

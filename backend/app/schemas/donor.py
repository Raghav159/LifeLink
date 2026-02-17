from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
import uuid


class DonorBase(BaseModel):
    name: str = Field(..., example="Raghav")
    age: int = Field(..., gt=18, example=25)
    blood_group: str = Field(..., example="O+")
    latitude: float
    longitude: float
    available: bool = True
    last_donation_date: date
    contact_number: str
    health_eligible: bool = True


class DonorCreate(DonorBase):
    pass


class DonorUpdate(BaseModel):
    available: Optional[bool] = None
    health_eligible: Optional[bool] = None


class DonorResponse(DonorBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

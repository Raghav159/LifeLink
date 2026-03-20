from pydantic import BaseModel
import uuid


class DonorMatchResult(BaseModel):
    """Result of donor matching for a blood request"""
    donor_id: uuid.UUID
    name: str
    blood_group: str
    distance_km: float
    ml_score: float
    
    class Config:
        from_attributes = True

from pydantic import BaseModel
import uuid


class DonorMatchResult(BaseModel):
    """Result of donor matching for a blood request"""
    donor_id: uuid.UUID
    name: str
    age: int
    blood_group: str
    contact_number: str
    latitude: float
    longitude: float
    distance_km: float
    ml_score: float
    last_donation_date: str
    health_eligible: bool
    available: bool
    donation_frequency_6m: int
    successful_previous_matches: int
    has_adverse_reactions: bool
    
    class Config:
        from_attributes = True

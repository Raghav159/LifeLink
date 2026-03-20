import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base


class Donor(Base):
    __tablename__ = "donors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    blood_group = Column(String(5), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    available = Column(Boolean, default=True)
    last_donation_date = Column(Date, nullable=False)

    contact_number = Column(String(15), nullable=False)
    health_eligible = Column(Boolean, default=True)
    
    # ML-related fields
    donation_frequency_6m = Column(Integer, default=0)
    successful_previous_matches = Column(Integer, default=0)
    has_adverse_reactions = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

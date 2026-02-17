from sqlalchemy.orm import Session
from app.models.donor import Donor
from app.schemas.donor import DonorCreate, DonorUpdate
import uuid


def create_donor(db: Session, donor: DonorCreate):
    db_donor = Donor(**donor.model_dump())
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor


def get_donor(db: Session, donor_id: uuid.UUID):
    return db.query(Donor).filter(Donor.id == donor_id).first()


def get_all_donors(db: Session):
    return db.query(Donor).all()


def update_donor(db: Session, donor_id: uuid.UUID, donor_update: DonorUpdate):
    db_donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not db_donor:
        return None

    update_data = donor_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_donor, key, value)

    db.commit()
    db.refresh(db_donor)
    return db_donor

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.schemas.donor import DonorCreate, DonorResponse, DonorUpdate
from app.services.donor_service import (
    create_donor,
    get_donor,
    get_all_donors,
    update_donor
)
import uuid

router = APIRouter(prefix="/donors", tags=["Donors"])


@router.post("/", response_model=DonorResponse)
def create_new_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    return create_donor(db, donor)


@router.get("/", response_model=list[DonorResponse])
def list_donors(db: Session = Depends(get_db)):
    return get_all_donors(db)


@router.get("/{donor_id}", response_model=DonorResponse)
def get_single_donor(donor_id: uuid.UUID, db: Session = Depends(get_db)):
    donor = get_donor(db, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor


@router.put("/{donor_id}", response_model=DonorResponse)
def update_single_donor(
    donor_id: uuid.UUID,
    donor_update: DonorUpdate,
    db: Session = Depends(get_db),
):
    donor = update_donor(db, donor_id, donor_update)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

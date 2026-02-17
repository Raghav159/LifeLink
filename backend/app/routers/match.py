from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.services.matching_service import match_donors
import uuid

router = APIRouter(prefix="/match", tags=["Matching"])


@router.get("/{request_id}")
def match(request_id: uuid.UUID, db: Session = Depends(get_db)):
    result = match_donors(db, request_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return result

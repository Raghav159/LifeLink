import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.services.matching_service import match_donors

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/match", tags=["Matching"])


# Import ml_model from main module
def get_ml_model():
    """Dependency to get the global ML model from main.py"""
    import app.main as main_module
    return main_module.ml_model


@router.get("/{request_id}", tags=["Matching"])
def match(
    request_id: UUID,
    db: Session = Depends(get_db),
    ml_model=Depends(get_ml_model)
):
    """
    Match donors for a blood request using ML ranking.
    
    Returns list of ranked donors sorted by ML score (highest first).
    """
    logger.info(f"Matching donors for request {request_id}...")
    
    result = match_donors(db, request_id, ml_model)

    if result is None:
        logger.warning(f"Request {request_id} not found")
        raise HTTPException(status_code=404, detail="Request not found")

    logger.info(f"Found {len(result)} matching donors")
    return result

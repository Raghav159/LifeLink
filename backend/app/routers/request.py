from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.schemas.request import RequestCreate, RequestResponse
from app.services.request_service import (
    create_request,
    get_request,
    get_all_requests,
)
import uuid

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("/", response_model=RequestResponse)
def create_new_request(request: RequestCreate, db: Session = Depends(get_db)):
    return create_request(db, request)


@router.get("/", response_model=list[RequestResponse])
def list_requests(db: Session = Depends(get_db)):
    return get_all_requests(db)


@router.get("/{request_id}", response_model=RequestResponse)
def get_single_request(request_id: uuid.UUID, db: Session = Depends(get_db)):
    request = get_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

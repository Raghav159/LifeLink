from sqlalchemy.orm import Session
from app.models.request import BloodRequest
from app.schemas.request import RequestCreate
import uuid


def create_request(db: Session, request: RequestCreate):
    db_request = BloodRequest(**request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_request(db: Session, request_id: uuid.UUID):
    return db.query(BloodRequest).filter(BloodRequest.id == request_id).first()


def get_all_requests(db: Session):
    return db.query(BloodRequest).all()

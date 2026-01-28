from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from database import SessionLocal
from models import Event
from schemas import EventCreate
from auth import verify_api_key

router = APIRouter(prefix="/v1/events")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def ingest_event(
    event: EventCreate,
    company_id: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    db_event = Event(
        event_id=str(uuid.uuid4()),
        company_id=company_id,
        customer_id=event.customer_id,
        user_id=event.user_id,
        event_name=event.event_name,
        properties=event.properties,
        timestamp=event.timestamp
    )

    db.add(db_event)
    db.commit()
    return {"status": "ok"}

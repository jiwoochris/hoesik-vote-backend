
from sqlalchemy.orm import Session
from app.repository.event_repository import create_event, get_all_events
from app.models.event import Event

def create_event_service(db: Session, name: str) -> Event:
	return create_event(db, name)

def get_all_events_service(db: Session) -> list[Event]:
	return get_all_events(db)

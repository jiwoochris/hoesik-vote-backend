
from sqlalchemy.orm import Session
from app.models.event import Event

def create_event(db: Session, name: str) -> Event:
	event = Event(name=name)
	db.add(event)
	db.commit()
	db.refresh(event)
	return event

def get_all_events(db: Session) -> list[Event]:
	return db.query(Event).all()

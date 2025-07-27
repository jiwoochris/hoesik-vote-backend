from sqlalchemy.orm import Session
from app.repository.vote_repository import create_vote, count_votes_by_event
from app.models.event import Vote

def create_vote_service(db: Session, event_id: int, menu_id: int) -> Vote:
	return create_vote(db, event_id, menu_id)

def count_votes_by_event_service(db: Session, event_id: int) -> list[tuple]:
	return count_votes_by_event(db, event_id)
from sqlalchemy.orm import Session
from app.repository.vote_repository import create_vote, get_vote_results
from app.models.vote import Vote

def create_vote_service(db: Session, event_id: int, menu_id: int) -> Vote:
	return create_vote(db, event_id, menu_id)

def get_vote_results_service(db: Session, event_id: int) -> list[dict]:
	return get_vote_results(db, event_id)

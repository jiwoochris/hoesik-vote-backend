from sqlalchemy.orm import Session
from app.models.event import Vote

def create_vote(db: Session, event_id: int, menu_id: int) -> Vote:
	vote = Vote(event_id=event_id, menu_id=menu_id)
	db.add(vote)
	db.commit()
	db.refresh(vote)
	return vote

def count_votes_by_event(db: Session, event_id: int) -> list[tuple]:
	from app.models.event import Menu
	# 메뉴별 투표수 집계
	return db.query(Vote.menu_id, Menu.name, db.func.count(Vote.id))\
		.join(Menu, Vote.menu_id == Menu.id)\
		.filter(Vote.event_id == event_id)\
		.group_by(Vote.menu_id, Menu.name)\
		.all()
from sqlalchemy.orm import Session
from app.models.vote import Vote

def create_vote(db: Session, event_id: int, menu_id: int) -> Vote:
	vote = Vote(event_id=event_id, menu_id=menu_id)
	db.add(vote)
	db.commit()
	db.refresh(vote)
	return vote

def get_vote_results(db: Session, event_id: int) -> list[dict]:
	from app.models.menu import Menu
	from sqlalchemy import func
	results = (
		db.query(Vote.menu_id, Menu.name, func.count(Vote.id).label("votes"))
		.join(Menu, Vote.menu_id == Menu.id)
		.filter(Vote.event_id == event_id)
		.group_by(Vote.menu_id, Menu.name)
		.all()
	)
	return [
		{"menu_id": r.menu_id, "name": r.name, "votes": r.votes}
		for r in results
	]

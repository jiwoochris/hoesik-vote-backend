
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.event import (
	EventCreate, EventResponse,
	MenuCreate, MenuResponse,
	VoteCreate, VoteResponse,
	ResultResponse
)
from app.service.event_service import create_event_service, get_all_events_service
from app.service.menu_service import create_menu_service, get_menus_by_event_service
from app.service.vote_service import create_vote_service, count_votes_by_event_service
from app.db import get_db

router = APIRouter()

@router.post("/api/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
	payload: EventCreate,
	db: Session = Depends(get_db),
) -> EventResponse:
	event = create_event_service(db, payload.name)
	return EventResponse(event_id=int(event.id), name=str(event.name))


# 회식 이벤트 목록 조회
@router.get("/api/events", response_model=List[EventResponse], status_code=status.HTTP_200_OK)
def list_events(db: Session = Depends(get_db)) -> List[EventResponse]:
	events = get_all_events_service(db)
	return [EventResponse(event_id=int(e.id), name=str(e.name)) for e in events]


# 메뉴 후보 제안
@router.post("/api/events/{event_id}/menus", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(event_id: int, payload: MenuCreate, db: Session = Depends(get_db)) -> MenuResponse:
	menu = create_menu_service(db, event_id, payload.name)
	return MenuResponse(id=int(menu.id), event_id=int(menu.event_id), name=str(menu.name))

# 메뉴 후보 목록 조회
@router.get("/api/events/{event_id}/menus", response_model=List[MenuResponse], status_code=status.HTTP_200_OK)
def list_menus(event_id: int, db: Session = Depends(get_db)) -> List[MenuResponse]:
	menus = get_menus_by_event_service(db, event_id)
	return [MenuResponse(id=int(m.id), event_id=int(m.event_id), name=str(m.name)) for m in menus]

# 메뉴 후보에 투표
@router.post("/api/events/{event_id}/votes", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
def create_vote(event_id: int, payload: VoteCreate, db: Session = Depends(get_db)) -> VoteResponse:
	vote = create_vote_service(db, event_id, payload.menu_id)
	return VoteResponse(vote_id=int(vote.id), event_id=int(vote.event_id), menu_id=int(vote.menu_id))

# 투표 현황/결과 조회
@router.get("/api/events/{event_id}/results", response_model=List[ResultResponse], status_code=status.HTTP_200_OK)
def get_results(event_id: int, db: Session = Depends(get_db)) -> List[ResultResponse]:
	results = count_votes_by_event_service(db, event_id)
	return [ResultResponse(menu_id=int(menu_id), name=str(name), votes=int(votes)) for menu_id, name, votes in results]

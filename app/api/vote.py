from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.vote import VoteCreate, VoteResponse
from app.service.vote_service import create_vote_service, get_vote_results_service
from app.db import get_db

router = APIRouter()

@router.post("/api/events/{event_id}/votes", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
def create_vote(event_id: int, payload: VoteCreate, db: Session = Depends(get_db)) -> VoteResponse:
	vote = create_vote_service(db, event_id, payload.menu_id)
	return VoteResponse(vote_id=int(vote.id), event_id=int(vote.event_id), menu_id=int(vote.menu_id))

@router.get("/api/events/{event_id}/results", status_code=status.HTTP_200_OK)
def get_results(event_id: int, db: Session = Depends(get_db)):
	return get_vote_results_service(db, event_id)

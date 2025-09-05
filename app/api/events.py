from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.service.event import EventService

router = APIRouter(prefix="/api", tags=["events"])


@router.post(
	"/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED
)
async def create_event(event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_db)) -> EventResponse:
	"""새로운 회식 이벤트를 생성합니다."""
	service = EventService(db)
	return await service.create_event(event)


@router.get("/events", response_model=list[EventResponse])
async def get_events(db: AsyncIOMotorDatabase = Depends(get_db)) -> list[EventResponse]:
	"""Retrieve all created company dinner events."""
	service = EventService(db)
	return await service.get_all_events()

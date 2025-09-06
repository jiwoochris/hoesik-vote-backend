from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.schemas.menu import (
    MenuCreate,
    MenuResponse,
    VoteCreate,
    VoteResponse,
    VoteResult,
)
from app.service.event import EventService
from app.service.menu import MenuService
from app.service.vote import VoteService

router = APIRouter(prefix="/api", tags=["events"])


@router.post(
    "/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED
)
async def create_event(
    event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_db)
) -> EventResponse:
    """새로운 회식 이벤트를 생성합니다."""
    service = EventService(db)
    return await service.create_event(event)


@router.get("/events", response_model=list[EventResponse])
async def get_events(db: AsyncIOMotorDatabase = Depends(get_db)) -> list[EventResponse]:
    """생성된 모든 회식 이벤트를 조회합니다."""
    service = EventService(db)
    return await service.get_all_events()


@router.post(
    "/events/{event_id}/menus",
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    event_id: str, menu: MenuCreate, db: AsyncIOMotorDatabase = Depends(get_db)
) -> MenuResponse:
    """특정 회식 이벤트에 메뉴 후보를 제안합니다."""
    service = MenuService(db)
    return await service.create_menu(event_id, menu)


@router.get("/events/{event_id}/menus", response_model=list[MenuResponse])
async def get_menus(
    event_id: str, db: AsyncIOMotorDatabase = Depends(get_db)
) -> list[MenuResponse]:
    """특정 이벤트에 제안된 모든 메뉴 후보를 조회합니다."""
    service = MenuService(db)
    return await service.get_menus_by_event_id(event_id)


@router.post(
    "/events/{event_id}/votes",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_vote(
    event_id: str, vote: VoteCreate, db: AsyncIOMotorDatabase = Depends(get_db)
) -> VoteResponse:
    """특정 이벤트의 메뉴 후보에 투표합니다."""
    service = VoteService(db)
    return await service.create_vote(event_id, vote)


@router.get("/events/{event_id}/results", response_model=list[VoteResult])
async def get_vote_results(
    event_id: str, db: AsyncIOMotorDatabase = Depends(get_db)
) -> list[VoteResult]:
    """특정 이벤트의 각 메뉴 후보별 투표 수를 조회합니다."""
    service = VoteService(db)
    return await service.get_vote_results_by_event_id(event_id)

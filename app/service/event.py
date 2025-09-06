from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repository.event import EventRepository
from app.schemas.event import EventCreate, EventResponse


class EventService:
    """이벤트 관련 비즈니스 로직을 처리하는 서비스 클래스입니다."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = EventRepository(db)

    async def create_event(self, event: EventCreate) -> EventResponse:
        """새로운 이벤트를 생성합니다."""
        db_event = await self.repository.create_event(event)
        return EventResponse(event_id=db_event.id, name=db_event.name)

    async def get_all_events(self) -> list[EventResponse]:
        """모든 이벤트를 조회합니다."""
        events = await self.repository.get_all_events()
        return [EventResponse(event_id=event.id, name=event.name) for event in events]

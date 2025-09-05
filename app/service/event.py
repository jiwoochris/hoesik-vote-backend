from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repository.event import EventRepository
from app.schemas.event import EventCreate, EventResponse


class EventService:
	"""
	이벤트 관련 비즈니스 로직을 처리하는 서비스 클래스입니다.

	이 클래스는 이벤트의 생성, 조회 등의 비즈니스 로직을 담당하며,
	EventRepository를 통해 데이터베이스와 상호작용합니다.

	Attributes:
		repository (EventRepository): 이벤트 데이터 접근을 위한 리포지토리 인스턴스

	Methods:
		create_event(event: EventCreate) -> EventResponse:
			새로운 이벤트를 생성하고 생성된 이벤트 정보를 반환합니다.
		
		get_all_events() -> list[EventResponse]:
			시스템에 등록된 모든 이벤트 목록을 조회하여 반환합니다.

	Example:
		>>> from motor.motor_asyncio import AsyncIOMotorDatabase
		>>> event_service = EventService(db)
		>>> new_event = EventCreate(name="신년 이벤트")
		>>> created_event = await event_service.create_event(new_event)
		>>> all_events = await event_service.get_all_events()
	"""
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

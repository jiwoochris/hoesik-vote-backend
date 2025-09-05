from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
	"""이벤트 데이터 접근 계층."""

	def __init__(self, db: AsyncIOMotorDatabase):
		self.db = db
		self.collection = db.events

	async def create_event(self, event: EventCreate) -> Event:
		"""새로운 이벤트를 생성합니다."""
		event_dict = event.model_dump()
		result = await self.collection.insert_one(event_dict)
		event_dict["_id"] = str(result.inserted_id)
		return Event(**event_dict)

	async def get_all_events(self) -> List[Event]:
		"""모든 이벤트를 조회합니다."""
		cursor = self.collection.find({})
		events = []
		async for document in cursor:
			document["_id"] = str(document["_id"])
			events.append(Event(**document))
		return events

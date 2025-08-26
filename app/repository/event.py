from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate


class EventRepository:
	"""이벤트 데이터 접근 계층."""

	def __init__(self, db: Session):
		self.db = db

	def create_event(self, event: EventCreate) -> Event:
		"""새로운 이벤트를 생성합니다."""
		db_event = Event(**event.dict())
		self.db.add(db_event)
		self.db.commit()
		self.db.refresh(db_event)
		return db_event

	def get_all_events(self) -> list[Event]:
		"""모든 이벤트를 조회합니다."""
		return self.db.query(Event).all()

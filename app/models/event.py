from sqlalchemy import Column, Integer, String

from app.database import Base


class Event(Base):
	"""회식 이벤트 모델."""

	__tablename__ = "events"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)

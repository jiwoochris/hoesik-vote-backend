from pydantic import BaseModel


class EventCreate(BaseModel):
	"""이벤트 생성 요청 스키마."""

	name: str


class EventResponse(BaseModel):
	"""이벤트 응답 스키마."""

	event_id: int
	name: str

	class Config:
		from_attributes = True

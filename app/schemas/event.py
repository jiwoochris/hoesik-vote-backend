from pydantic import BaseModel, ConfigDict
from typing import Union


class EventCreate(BaseModel):
	"""이벤트 생성 요청 스키마."""

	name: str


class EventResponse(BaseModel):
	"""이벤트 응답 스키마."""

	event_id: Union[str, int]  # MongoDB ObjectId는 문자열로, 테스트에서는 정수로 처리
	name: str

	model_config = ConfigDict(from_attributes=True)

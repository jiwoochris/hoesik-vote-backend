from pydantic import BaseModel, Field
from typing import Optional


class Event(BaseModel):
	"""회식 이벤트 모델."""

	id: Optional[str] = Field(default=None, alias="_id")
	name: str

	model_config = {
		"populate_by_name": True,
		"arbitrary_types_allowed": True
	}

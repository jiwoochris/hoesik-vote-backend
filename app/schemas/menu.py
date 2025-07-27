from pydantic import BaseModel

class MenuCreate(BaseModel):
	name: str

class MenuResponse(BaseModel):
	id: int
	event_id: int
	name: str

	class Config:
		orm_mode = True

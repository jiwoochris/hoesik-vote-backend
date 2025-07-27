from pydantic import BaseModel


class EventCreate(BaseModel):
	name: str

class EventResponse(BaseModel):
	event_id: int
	name: str

	class Config:
		orm_mode = True


# 메뉴 후보
class MenuCreate(BaseModel):
	name: str

class MenuResponse(BaseModel):
	id: int
	event_id: int
	name: str

	class Config:
		orm_mode = True


# 투표
class VoteCreate(BaseModel):
	menu_id: int

class VoteResponse(BaseModel):
	vote_id: int
	event_id: int
	menu_id: int

	class Config:
		orm_mode = True


# 결과
class ResultResponse(BaseModel):
	menu_id: int
	name: str
	votes: int

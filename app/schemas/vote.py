from pydantic import BaseModel

class VoteCreate(BaseModel):
	menu_id: int

class VoteResponse(BaseModel):
	vote_id: int
	event_id: int
	menu_id: int

	class Config:
		orm_mode = True


from pydantic import BaseModel, Field


class Vote(BaseModel):
    """투표 모델."""

    vote_id: str | None = Field(default=None, alias="_id")
    event_id: str
    menu_id: str

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}

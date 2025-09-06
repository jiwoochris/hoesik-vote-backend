
from pydantic import BaseModel, Field


class Menu(BaseModel):
    """메뉴 후보 모델."""

    id: str | None = Field(default=None, alias="_id")
    event_id: str
    name: str

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}

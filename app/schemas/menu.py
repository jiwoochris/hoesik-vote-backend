
from pydantic import BaseModel, ConfigDict


class MenuCreate(BaseModel):
    """메뉴 생성 요청 스키마."""

    name: str


class MenuResponse(BaseModel):
    """메뉴 응답 스키마."""

    id: str | int  # MongoDB ObjectId는 문자열로, 테스트에서는 정수로 처리
    event_id: str | int
    name: str

    model_config = ConfigDict(from_attributes=True)


class VoteCreate(BaseModel):
    """투표 생성 요청 스키마."""

    menu_id: str | int


class VoteResponse(BaseModel):
    """투표 응답 스키마."""

    vote_id: str | int
    event_id: str | int
    menu_id: str | int

    model_config = ConfigDict(from_attributes=True)


class VoteResult(BaseModel):
    """투표 결과 스키마."""

    menu_id: str | int
    name: str
    votes: int

    model_config = ConfigDict(from_attributes=True)

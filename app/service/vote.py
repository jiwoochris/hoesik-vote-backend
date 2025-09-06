from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repository.menu import MenuRepository
from app.repository.vote import VoteRepository
from app.schemas.menu import VoteCreate, VoteResponse, VoteResult
from app.utils import validate_event_exists


class VoteService:
    """투표 관련 비즈니스 로직을 처리하는 서비스 클래스입니다."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.vote_repository = VoteRepository(db)
        self.menu_repository = MenuRepository(db)
        self.db = db

    async def create_vote(self, event_id: str, vote: VoteCreate) -> VoteResponse:
        """특정 이벤트의 메뉴에 투표합니다."""
        await validate_event_exists(self.db, event_id)

        # 메뉴 존재 확인
        menu = await self.menu_repository.get_menu_by_id(str(vote.menu_id))
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
            )

        # 메뉴가 해당 이벤트에 속하는지 확인
        if menu.event_id != event_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu does not belong to this event",
            )

        db_vote = await self.vote_repository.create_vote(event_id, vote)
        return VoteResponse(
            vote_id=db_vote.vote_id, event_id=db_vote.event_id, menu_id=db_vote.menu_id
        )

    async def get_vote_results_by_event_id(self, event_id: str) -> list[VoteResult]:
        """특정 이벤트의 투표 결과를 조회합니다."""
        await validate_event_exists(self.db, event_id)
        return await self.vote_repository.get_vote_results_by_event_id(event_id)


from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.vote import Vote
from app.schemas.menu import VoteCreate, VoteResult


class VoteRepository:
    """투표 데이터 접근 계층."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.votes

    async def create_vote(self, event_id: str, vote: VoteCreate) -> Vote:
        """새로운 투표를 생성합니다."""
        vote_dict = vote.model_dump()
        vote_dict["event_id"] = event_id
        # menu_id를 문자열로 변환 (MongoDB ObjectId 호환성)
        vote_dict["menu_id"] = str(vote_dict["menu_id"])
        result = await self.collection.insert_one(vote_dict)
        vote_dict["_id"] = str(result.inserted_id)
        return Vote(**vote_dict)

    async def get_vote_results_by_event_id(self, event_id: str) -> list[VoteResult]:
        """특정 이벤트의 투표 결과를 집계합니다."""
        pipeline = [
            {"$match": {"event_id": event_id}},
            {"$group": {"_id": "$menu_id", "votes": {"$sum": 1}}},
            {
                "$lookup": {
                    "from": "menus",
                    "let": {"menu_id": {"$toObjectId": "$_id"}},
                    "pipeline": [{"$match": {"$expr": {"$eq": ["$_id", "$$menu_id"]}}}],
                    "as": "menu_info",
                }
            },
            {"$unwind": "$menu_info"},
            {
                "$project": {
                    "menu_id": "$_id",
                    "name": "$menu_info.name",
                    "votes": 1,
                    "_id": 0,
                }
            },
            {"$sort": {"votes": -1}},  # 투표수 내림차순 정렬
        ]

        results = []
        async for doc in self.collection.aggregate(pipeline):
            results.append(
                VoteResult(menu_id=doc["menu_id"], name=doc["name"], votes=doc["votes"])
            )

        # 투표가 없는 메뉴들도 포함하기 위해 메뉴 컬렉션에서 추가 조회
        menus_cursor = self.db.menus.find({"event_id": event_id})
        voted_menu_ids = {result.menu_id for result in results}

        async for menu_doc in menus_cursor:
            menu_id = str(menu_doc["_id"])
            if menu_id not in voted_menu_ids:
                results.append(
                    VoteResult(menu_id=menu_id, name=menu_doc["name"], votes=0)
                )

        # 투표수 기준으로 다시 정렬
        results.sort(key=lambda x: x.votes, reverse=True)
        return results

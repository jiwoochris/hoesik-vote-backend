from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase


async def validate_event_exists(db: AsyncIOMotorDatabase, event_id: str) -> None:
    """이벤트가 존재하는지 확인합니다."""
    try:
        event_object_id = ObjectId(event_id)
        event_doc = await db.events.find_one({"_id": event_object_id})
    except InvalidId:
        # 테스트 환경에서는 단순 문자열 ID 사용
        event_doc = await db.events.find_one({"_id": event_id})

    if not event_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )


from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.menu import Menu
from app.schemas.menu import MenuCreate


class MenuRepository:
    """메뉴 데이터 접근 계층."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.menus

    async def create_menu(self, event_id: str, menu: MenuCreate) -> Menu:
        """새로운 메뉴 후보를 생성합니다."""
        menu_dict = menu.model_dump()
        menu_dict["event_id"] = event_id
        result = await self.collection.insert_one(menu_dict)
        menu_dict["_id"] = str(result.inserted_id)
        return Menu(**menu_dict)

    async def get_menus_by_event_id(self, event_id: str) -> list[Menu]:
        """특정 이벤트의 모든 메뉴 후보를 조회합니다."""
        cursor = self.collection.find({"event_id": event_id})
        menus = []
        async for document in cursor:
            document["_id"] = str(document["_id"])
            menus.append(Menu(**document))
        return menus

    async def get_menu_by_id(self, menu_id: str) -> Menu:
        """특정 메뉴를 ID로 조회합니다."""
        from bson import ObjectId
        from bson.errors import InvalidId

        try:
            document = await self.collection.find_one({"_id": ObjectId(menu_id)})
        except InvalidId:
            # 테스트 환경에서는 단순 문자열 ID 사용
            document = await self.collection.find_one({"_id": menu_id})

        if document:
            document["_id"] = str(document["_id"])
            return Menu(**document)
        return None

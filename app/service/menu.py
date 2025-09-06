from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repository.menu import MenuRepository
from app.schemas.menu import MenuCreate, MenuResponse
from app.utils import validate_event_exists


class MenuService:
    """메뉴 관련 비즈니스 로직을 처리하는 서비스 클래스입니다."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.menu_repository = MenuRepository(db)
        self.db = db

    async def create_menu(self, event_id: str, menu: MenuCreate) -> MenuResponse:
        """특정 이벤트에 새로운 메뉴 후보를 생성합니다."""
        await validate_event_exists(self.db, event_id)
        db_menu = await self.menu_repository.create_menu(event_id, menu)
        return MenuResponse(id=db_menu.id, event_id=db_menu.event_id, name=db_menu.name)

    async def get_menus_by_event_id(self, event_id: str) -> list[MenuResponse]:
        """특정 이벤트의 모든 메뉴 후보를 조회합니다."""
        await validate_event_exists(self.db, event_id)
        menus = await self.menu_repository.get_menus_by_event_id(event_id)
        return [
            MenuResponse(id=menu.id, event_id=menu.event_id, name=menu.name)
            for menu in menus
        ]

from sqlalchemy.orm import Session
from app.repository.menu_repository import create_menu, get_menus_by_event
from app.models.event import Menu

def create_menu_service(db: Session, event_id: int, name: str) -> Menu:
	return create_menu(db, event_id, name)

def get_menus_by_event_service(db: Session, event_id: int) -> list[Menu]:
	return get_menus_by_event(db, event_id)
from sqlalchemy.orm import Session
from app.repository.menu_repository import create_menu, get_menus_by_event
from app.models.menu import Menu

def create_menu_service(db: Session, event_id: int, name: str) -> Menu:
	return create_menu(db, event_id, name)

def get_menus_by_event_service(db: Session, event_id: int) -> list[Menu]:
	return get_menus_by_event(db, event_id)

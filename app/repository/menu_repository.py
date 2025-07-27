from sqlalchemy.orm import Session
from app.models.event import Menu

def create_menu(db: Session, event_id: int, name: str) -> Menu:
	menu = Menu(event_id=event_id, name=name)
	db.add(menu)
	db.commit()
	db.refresh(menu)
	return menu

def get_menus_by_event(db: Session, event_id: int) -> list[Menu]:
	return db.query(Menu).filter(Menu.event_id == event_id).all()
from sqlalchemy.orm import Session
from app.models.menu import Menu

def create_menu(db: Session, event_id: int, name: str) -> Menu:
	menu = Menu(event_id=event_id, name=name)
	db.add(menu)
	db.commit()
	db.refresh(menu)
	return menu

def get_menus_by_event(db: Session, event_id: int) -> list[Menu]:
	return db.query(Menu).filter(Menu.event_id == event_id).all()

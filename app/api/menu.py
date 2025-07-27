from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.menu import MenuCreate, MenuResponse
from app.service.menu_service import create_menu_service, get_menus_by_event_service
from app.db import get_db

router = APIRouter()

@router.post("/api/events/{event_id}/menus", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(event_id: int, payload: MenuCreate, db: Session = Depends(get_db)) -> MenuResponse:
	menu = create_menu_service(db, event_id, payload.name)
	return MenuResponse(id=int(menu.id), event_id=int(menu.event_id), name=str(menu.name))

@router.get("/api/events/{event_id}/menus", response_model=List[MenuResponse], status_code=status.HTTP_200_OK)
def list_menus(event_id: int, db: Session = Depends(get_db)) -> List[MenuResponse]:
	menus = get_menus_by_event_service(db, event_id)
	return [MenuResponse(id=int(m.id), event_id=int(m.event_id), name=str(m.name)) for m in menus]

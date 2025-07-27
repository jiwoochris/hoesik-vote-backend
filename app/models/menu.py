from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from app.models.event import Base

class Menu(Base):
	__tablename__ = "menus"

	id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
	name = Column(String, nullable=False)

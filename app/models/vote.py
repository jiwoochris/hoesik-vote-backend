from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from app.models.event import Base

class Vote(Base):
	__tablename__ = "votes"

	id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
	menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, index=True)

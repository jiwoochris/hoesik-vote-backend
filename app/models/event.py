from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # type: ignore


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    menu_id = Column(Integer, nullable=False, index=True)

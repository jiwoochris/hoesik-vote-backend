from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.event import Base
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

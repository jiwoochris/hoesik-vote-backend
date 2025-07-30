import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# 테스트용 인메모리 SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
	"""모든 테스트 전후에 데이터베이스를 초기화합니다."""
	# Given: 테스트 시작 전 데이터베이스 테이블 생성
	Base.metadata.create_all(bind=engine)
	yield
	# Cleanup: 테스트 후 데이터베이스 테이블 삭제
	Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
	"""FastAPI TestClient를 제공합니다."""
	return TestClient(app)

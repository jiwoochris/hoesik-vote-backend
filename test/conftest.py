import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock

from app.database import get_db
from app.main import app

# Mock 이벤트 ID 카운터
event_id_counter = 0


def get_next_event_id():
	"""순차적으로 이벤트 ID를 생성합니다."""
	global event_id_counter
	event_id_counter += 1
	return event_id_counter


class MockCollection:
	"""Mock MongoDB 컬렉션."""
	
	def __init__(self):
		self.documents = []
	
	async def insert_one(self, document):
		"""문서 삽입 시뮬레이션."""
		event_id = get_next_event_id()
		document["_id"] = str(event_id)
		self.documents.append(document.copy())
		
		result = Mock()
		result.inserted_id = str(event_id)
		return result
	
	def find(self, query):
		"""문서 조회 시뮬레이션."""
		return MockCursor(self.documents)


class MockCursor:
	"""Mock MongoDB 커서."""
	
	def __init__(self, documents):
		self.documents = documents
		self.index = 0
	
	def __aiter__(self):
		return self
	
	async def __anext__(self):
		if self.index >= len(self.documents):
			raise StopAsyncIteration
		document = self.documents[self.index]
		self.index += 1
		return document


class MockDatabase:
	"""Mock MongoDB 데이터베이스."""
	
	def __init__(self):
		self.events = MockCollection()


# 전역 Mock 데이터베이스
mock_database = MockDatabase()


async def override_get_db():
	"""테스트용 Mock 데이터베이스를 반환합니다."""
	yield mock_database


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
	"""모든 테스트 전후에 데이터베이스를 초기화합니다."""
	global event_id_counter
	
	# Given: 테스트 시작 전 Mock 데이터베이스 초기화
	mock_database.events.documents.clear()
	event_id_counter = 0
	
	yield
	
	# Cleanup: 테스트 후 Mock 데이터베이스 초기화
	mock_database.events.documents.clear()
	event_id_counter = 0


@pytest.fixture
def client():
	"""FastAPI TestClient를 제공합니다."""
	return TestClient(app)

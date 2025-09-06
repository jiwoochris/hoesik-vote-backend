from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app

# Mock ID 카운터들
event_id_counter = 0
menu_id_counter = 0
vote_id_counter = 0


def get_next_event_id():
    """순차적으로 이벤트 ID를 생성합니다."""
    global event_id_counter
    event_id_counter += 1
    return event_id_counter


def get_next_menu_id():
    """순차적으로 메뉴 ID를 생성합니다."""
    global menu_id_counter
    menu_id_counter += 1
    return menu_id_counter


def get_next_vote_id():
    """순차적으로 투표 ID를 생성합니다."""
    global vote_id_counter
    vote_id_counter += 1
    return vote_id_counter


class MockCollection:
    """Mock MongoDB 컬렉션."""

    def __init__(self, collection_type="events"):
        self.documents = []
        self.collection_type = collection_type

    async def insert_one(self, document):
        """문서 삽입 시뮬레이션."""
        if self.collection_type == "events":
            doc_id = get_next_event_id()
        elif self.collection_type == "menus":
            doc_id = get_next_menu_id()
        elif self.collection_type == "votes":
            doc_id = get_next_vote_id()
        else:
            doc_id = len(self.documents) + 1

        document["_id"] = str(doc_id)
        self.documents.append(document.copy())

        result = Mock()
        result.inserted_id = str(doc_id)
        return result

    def find(self, query):
        """문서 조회 시뮬레이션."""
        filtered_docs = []
        for doc in self.documents:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                filtered_docs.append(doc)
        return MockCursor(filtered_docs)

    async def find_one(self, query):
        """단일 문서 조회 시뮬레이션."""
        from bson import ObjectId

        for doc in self.documents:
            match = True
            for key, value in query.items():
                if key == "_id":
                    # ObjectId 또는 문자열 ID 처리
                    if isinstance(value, ObjectId):
                        if doc.get("_id") != str(value):
                            match = False
                            break
                    else:
                        if doc.get("_id") != str(value):
                            match = False
                            break
                elif key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                return doc
        return None

    def aggregate(self, pipeline):
        """집계 쿼리 시뮬레이션."""
        return MockAggregationCursor(self.documents, pipeline, mock_database)


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


class MockAggregationCursor:
    """Mock MongoDB 집계 커서."""

    def __init__(self, documents, pipeline, db=None):
        self.documents = documents
        self.pipeline = pipeline
        self.index = 0
        self.db = db
        self.result = self._execute_pipeline()

    def _execute_pipeline(self):
        """간단한 집계 파이프라인 시뮬레이션."""
        result = []
        # 간단한 $match와 $group 지원
        for stage in self.pipeline:
            if "$match" in stage:
                # 여기서는 event_id 매치만 시뮬레이션
                event_id = stage["$match"].get("event_id")
                if event_id:
                    vote_docs = [
                        doc for doc in self.documents if doc.get("event_id") == event_id
                    ]

                    # 투표 결과 집계
                    vote_counts = {}
                    for vote in vote_docs:
                        menu_id = vote.get("menu_id")
                        if menu_id:
                            vote_counts[menu_id] = vote_counts.get(menu_id, 0) + 1

                    # 메뉴 정보 조회 (전역 mock_database 사용)
                    for menu_id, votes in vote_counts.items():
                        menu_doc = None
                        for doc in mock_database.menus.documents:
                            if doc.get("_id") == str(menu_id):
                                menu_doc = doc
                                break
                        if menu_doc:
                            result.append(
                                {
                                    "menu_id": menu_id,
                                    "name": menu_doc.get("name"),
                                    "votes": votes,
                                }
                            )

        # 투표수 내림차순 정렬
        result.sort(key=lambda x: x["votes"], reverse=True)
        return result

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.result):
            raise StopAsyncIteration
        item = self.result[self.index]
        self.index += 1
        return item


class MockDatabase:
    """Mock MongoDB 데이터베이스."""

    def __init__(self):
        self.events = MockCollection("events")
        self.menus = MockCollection("menus")
        self.votes = MockCollection("votes")


# 전역 Mock 데이터베이스
mock_database = MockDatabase()


async def override_get_db():
    """테스트용 Mock 데이터베이스를 반환합니다."""
    yield mock_database


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """모든 테스트 전후에 데이터베이스를 초기화합니다."""
    global event_id_counter, menu_id_counter, vote_id_counter

    # Given: 테스트 시작 전 Mock 데이터베이스 초기화
    mock_database.events.documents.clear()
    mock_database.menus.documents.clear()
    mock_database.votes.documents.clear()
    event_id_counter = 0
    menu_id_counter = 0
    vote_id_counter = 0

    yield

    # Cleanup: 테스트 후 Mock 데이터베이스 초기화
    mock_database.events.documents.clear()
    mock_database.menus.documents.clear()
    mock_database.votes.documents.clear()
    event_id_counter = 0
    menu_id_counter = 0
    vote_id_counter = 0


@pytest.fixture
def client():
    """FastAPI TestClient를 제공합니다."""
    return TestClient(app)

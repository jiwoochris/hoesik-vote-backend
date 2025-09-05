import pytest
import pytest_asyncio
from unittest.mock import Mock, AsyncMock
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.service.event import EventService
from app.schemas.event import EventCreate, EventResponse
from app.models.event import Event
from bson import ObjectId

class TestEventService:
    """EventService 클래스의 테스트 케이스."""

    @pytest.fixture
    def mock_db(self):
        """Mock 데이터베이스를 생성합니다."""
        return Mock(spec=AsyncIOMotorDatabase)

    @pytest.fixture
    def event_service(self, mock_db):
        """EventService 인스턴스를 생성합니다."""
        return EventService(mock_db)

    @pytest.fixture
    def mock_event_create(self):
        """EventCreate 스키마 목 객체를 생성합니다."""
        return EventCreate(name="2025년 7월 회식")

    @pytest.fixture
    def mock_db_event(self):
        """DB Event 모델 목 객체를 생성합니다."""
        event = Event(id=ObjectId(), name="2025년 7월 회식")
        return event

    @pytest_asyncio.fixture
    async def test_create_event_success(self, event_service, mock_event_create, mock_db_event):
        """
        이벤트 생성이 성공적으로 완료되어야 한다.
        """
        # Given: EventRepository가 새로운 이벤트를 반환하도록 설정
        event_service.repository.create_event = AsyncMock(return_value=mock_db_event)

        # When: create_event 메서드를 호출한다
        result = await event_service.create_event(mock_event_create)

        # Then: EventResponse가 올바르게 반환되어야 한다
        assert isinstance(result, EventResponse)
        assert result.event_id == str(mock_db_event.id)
        assert result.name == "2025년 7월 회식"
        event_service.repository.create_event.assert_called_once_with(mock_event_create)

    @pytest_asyncio.fixture
    async def test_get_all_events_empty_list(self, event_service):
        """
        이벤트가 없을 때 빈 리스트를 반환해야 한다.
        """
        # Given: 데이터베이스에 이벤트가 없는 상태
        event_service.repository.get_all_events = AsyncMock(return_value=[])

        # When: get_all_events 메서드를 호출한다
        result = await event_service.get_all_events()

        # Then: 빈 리스트가 반환되어야 한다
        assert result == []
        event_service.repository.get_all_events.assert_called_once()

    @pytest_asyncio.fixture
    async def test_get_all_events_multiple_events(self, event_service):
        """
        여러 이벤트가 있을 때 모든 이벤트를 EventResponse 리스트로 반환해야 한다.
        """
        # Given: 데이터베이스에 여러 이벤트가 있는 상태
        event1 = Event(id=ObjectId(), name="2025년 7월 회식")
        event2 = Event(id=ObjectId(), name="2025년 8월 회식")
        
        event_service.repository.get_all_events = AsyncMock(return_value=[event1, event2])

        # When: get_all_events 메서드를 호출한다
        result = await event_service.get_all_events()

        # Then: 모든 이벤트가 EventResponse 형태로 반환되어야 한다
        assert len(result) == 2
        assert all(isinstance(event, EventResponse) for event in result)
        assert result[0].event_id == str(event1.id)
        assert result[0].name == "2025년 7월 회식"
        assert result[1].event_id == str(event2.id)
        assert result[1].name == "2025년 8월 회식"
        event_service.repository.get_all_events.assert_called_once()

    @pytest_asyncio.fixture
    async def test_get_all_events_single_event(self, event_service, mock_db_event):
        """
        하나의 이벤트가 있을 때 단일 EventResponse를 포함한 리스트를 반환해야 한다.
        """
        # Given: 데이터베이스에 하나의 이벤트가 있는 상태
        event_service.repository.get_all_events = AsyncMock(return_value=[mock_db_event])

        # When: get_all_events 메서드를 호출한다
        result = await event_service.get_all_events()

        # Then: 하나의 EventResponse가 포함된 리스트가 반환되어야 한다
        assert len(result) == 1
        assert isinstance(result[0], EventResponse)
        assert result[0].event_id == str(mock_db_event.id)
        assert result[0].name == "2025년 7월 회식"
        event_service.repository.get_all_events.assert_called_once()
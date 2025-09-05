import pytest
from fastapi.testclient import TestClient


def test_get_events_when_empty(client: TestClient):
	"""
	이벤트가 없을 때 빈 리스트를 반환해야 한다.
	"""
	# Given: 데이터베이스에 이벤트가 없는 상태

	# When: /api/events 엔드포인트에 GET 요청을 보낸다
	response = client.get("/api/events")

	# Then: 200 OK와 빈 리스트가 반환된다
	assert response.status_code == 200
	assert response.json() == []


def test_create_and_get_single_event(client: TestClient):
	"""
	이벤트를 생성하고 조회했을 때 올바른 데이터가 반환되어야 한다.
	"""
	# Given: 새로운 이벤트 데이터
	event_data = {"name": "2025년 7월 회식"}

	# When: 이벤트 생성 API를 호출한다
	create_response = client.post("/api/events", json=event_data)

	# Then: 201 Created 상태와 올바른 응답이 반환된다
	assert create_response.status_code == 201
	created_event = create_response.json()
	assert created_event["event_id"] == "1"
	assert created_event["name"] == "2025년 7월 회식"

	# When: 이벤트 목록 조회 API를 호출한다
	get_response = client.get("/api/events")

	# Then: 200 OK 상태와 생성된 이벤트가 포함된 리스트가 반환된다
	assert get_response.status_code == 200
	events = get_response.json()
	assert len(events) == 1
	assert events[0]["event_id"] == "1"
	assert events[0]["name"] == "2025년 7월 회식"


def test_create_multiple_events_and_get_all(client: TestClient):
	"""
	여러 이벤트를 생성하고 전체 목록을 조회했을 때 모든 이벤트가 반환되어야 한다.
	"""
	# Given: 여러 개의 이벤트 데이터
	events_data = [
		{"name": "2025년 7월 회식"},
		{"name": "2025년 8월 회식"},
		{"name": "2025년 9월 회식"}
	]

	# When: 여러 이벤트를 순차적으로 생성한다
	created_events = []
	for event_data in events_data:
		response = client.post("/api/events", json=event_data)
		assert response.status_code == 201
		created_events.append(response.json())

	# Then: 각 이벤트가 올바르게 생성되었는지 확인한다
	assert len(created_events) == 3
	for i, created_event in enumerate(created_events):
		assert created_event["event_id"] == str(i + 1)
		assert created_event["name"] == events_data[i]["name"]

	# When: 전체 이벤트 목록을 조회한다
	get_response = client.get("/api/events")

	# Then: 200 OK 상태와 모든 생성된 이벤트가 반환된다
	assert get_response.status_code == 200
	all_events = get_response.json()
	assert len(all_events) == 3
	
	# 생성 순서대로 정렬되어 반환되는지 확인
	for i, event in enumerate(all_events):
		assert event["event_id"] == str(i + 1)
		assert event["name"] == events_data[i]["name"]
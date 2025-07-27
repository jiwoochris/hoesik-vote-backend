from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_event_list_empty():
	"""
	이벤트가 없을 때 빈 리스트를 반환해야 한다.
	"""
	# Given: 데이터베이스에 이벤트가 없는 상태

	# When: /api/events 엔드포인트에 GET 요청을 보낸다
	response = client.get("/api/events")

	# Then: 200 OK와 빈 리스트가 반환된다
	assert response.status_code == 200
	assert response.json() == []

def test_event_list_multiple():
	"""
	여러 이벤트가 있을 때 전체 목록을 반환해야 한다.
	"""
	# Given: 여러 이벤트 생성
	data1 = {"name": "2025년 7월 회식"}
	data2 = {"name": "2025년 8월 회식"}
	client.post("/api/events", json=data1)
	client.post("/api/events", json=data2)

	# When: /api/events 엔드포인트에 GET 요청을 보낸다
	response = client.get("/api/events")

	# Then: 200 OK와 전체 이벤트 목록이 반환된다
	assert response.status_code == 200
	result = response.json()
	assert len(result) >= 2
	assert any(e["name"] == data1["name"] for e in result)
	assert any(e["name"] == data2["name"] for e in result)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
	"""
	새로운 회식 이벤트를 생성하면 201과 event_id, name이 반환되어야 한다.
	"""
	# Given: 이벤트 이름
	data = {"name": "2025년 7월 회식"}

	# When: /api/events에 POST 요청
	response = client.post("/api/events", json=data)

	# Then: 201, event_id, name 반환
	assert response.status_code == 201
	json_data = response.json()
	assert "event_id" in json_data
	assert json_data["name"] == data["name"]

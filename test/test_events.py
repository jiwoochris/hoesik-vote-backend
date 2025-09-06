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
        {"name": "2025년 9월 회식"},
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


def test_create_menu_for_event(client: TestClient):
    """
    특정 이벤트에 메뉴 후보를 제안할 수 있어야 한다.
    """
    # Given: 이벤트를 먼저 생성한다
    event_data = {"name": "2025년 7월 회식"}
    event_response = client.post("/api/events", json=event_data)
    assert event_response.status_code == 201
    event_id = event_response.json()["event_id"]

    # When: 메뉴 후보를 제안한다
    menu_data = {"name": "삼겹살"}
    menu_response = client.post(f"/api/events/{event_id}/menus", json=menu_data)

    # Then: 201 Created 상태와 올바른 응답이 반환된다
    if menu_response.status_code != 201:
        print(f"Error response: {menu_response.json()}")
    assert menu_response.status_code == 201
    created_menu = menu_response.json()
    assert created_menu["id"] == "1"
    assert created_menu["event_id"] == event_id
    assert created_menu["name"] == "삼겹살"


def test_get_menus_for_event(client: TestClient):
    """
    특정 이벤트의 메뉴 후보 목록을 조회할 수 있어야 한다.
    """
    # Given: 이벤트를 생성하고 여러 메뉴를 추가한다
    event_data = {"name": "2025년 7월 회식"}
    event_response = client.post("/api/events", json=event_data)
    event_id = event_response.json()["event_id"]

    menu_names = ["삼겹살", "치킨", "피자"]
    for menu_name in menu_names:
        menu_data = {"name": menu_name}
        client.post(f"/api/events/{event_id}/menus", json=menu_data)

    # When: 메뉴 목록을 조회한다
    response = client.get(f"/api/events/{event_id}/menus")

    # Then: 200 OK 상태와 모든 메뉴가 반환된다
    assert response.status_code == 200
    menus = response.json()
    assert len(menus) == 3
    for i, menu in enumerate(menus):
        assert menu["id"] == str(i + 1)
        assert menu["event_id"] == event_id
        assert menu["name"] == menu_names[i]


def test_create_vote_for_menu(client: TestClient):
    """
    특정 메뉴에 투표할 수 있어야 한다.
    """
    # Given: 이벤트와 메뉴를 생성한다
    event_data = {"name": "2025년 7월 회식"}
    event_response = client.post("/api/events", json=event_data)
    event_id = event_response.json()["event_id"]

    menu_data = {"name": "삼겹살"}
    menu_response = client.post(f"/api/events/{event_id}/menus", json=menu_data)
    menu_id = menu_response.json()["id"]

    # When: 메뉴에 투표한다
    vote_data = {"menu_id": menu_id}
    vote_response = client.post(f"/api/events/{event_id}/votes", json=vote_data)

    # Then: 201 Created 상태와 올바른 응답이 반환된다
    assert vote_response.status_code == 201
    created_vote = vote_response.json()
    assert created_vote["vote_id"] == "1"
    assert created_vote["event_id"] == event_id
    assert created_vote["menu_id"] == menu_id


def test_get_vote_results_for_event(client: TestClient):
    """
    특정 이벤트의 투표 결과를 조회할 수 있어야 한다.
    """
    # Given: 이벤트, 메뉴, 투표를 생성한다
    event_data = {"name": "2025년 7월 회식"}
    event_response = client.post("/api/events", json=event_data)
    event_id = event_response.json()["event_id"]

    # 여러 메뉴 생성
    menu1_response = client.post(
        f"/api/events/{event_id}/menus", json={"name": "삼겹살"}
    )
    menu2_response = client.post(f"/api/events/{event_id}/menus", json={"name": "치킨"})
    menu1_id = menu1_response.json()["id"]
    menu2_id = menu2_response.json()["id"]

    # 투표 생성 (삼겹살에 5표, 치킨에 3표)
    for _ in range(5):
        client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu1_id})
    for _ in range(3):
        client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu2_id})

    # When: 투표 결과를 조회한다
    response = client.get(f"/api/events/{event_id}/results")

    # Then: 200 OK 상태와 올바른 투표 결과가 반환된다
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2

    # 투표수 내림차순으로 정렬되어야 함
    assert results[0]["menu_id"] == menu1_id
    assert results[0]["name"] == "삼겹살"
    assert results[0]["votes"] == 5
    assert results[1]["menu_id"] == menu2_id
    assert results[1]["name"] == "치킨"
    assert results[1]["votes"] == 3


def test_vote_results_include_zero_vote_menus(client: TestClient):
    """
    투표를 받지 않은 메뉴도 결과에 포함되어야 한다.
    """
    # Given: 이벤트와 메뉴들을 생성하되 일부만 투표한다
    event_data = {"name": "2025년 7월 회식"}
    event_response = client.post("/api/events", json=event_data)
    event_id = event_response.json()["event_id"]

    menu1_response = client.post(
        f"/api/events/{event_id}/menus", json={"name": "삼겹살"}
    )
    client.post(f"/api/events/{event_id}/menus", json={"name": "치킨"})
    menu1_id = menu1_response.json()["id"]

    # 삼겹살에만 투표
    client.post(f"/api/events/{event_id}/votes", json={"menu_id": menu1_id})

    # When: 투표 결과를 조회한다
    response = client.get(f"/api/events/{event_id}/results")

    # Then: 투표를 받지 않은 메뉴도 0표로 포함되어야 한다
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2

    # 투표수 기준으로 정렬
    voted_menu = next(r for r in results if r["votes"] > 0)
    zero_vote_menu = next(r for r in results if r["votes"] == 0)

    assert voted_menu["name"] == "삼겹살"
    assert voted_menu["votes"] == 1
    assert zero_vote_menu["name"] == "치킨"
    assert zero_vote_menu["votes"] == 0


def test_error_cases(client: TestClient):
    """
    다양한 오류 상황들을 테스트한다.
    """
    # 존재하지 않는 이벤트에 메뉴 추가 시도
    response = client.post("/api/events/999/menus", json={"name": "삼겹살"})
    assert response.status_code == 404

    # 존재하지 않는 이벤트의 메뉴 조회 시도
    response = client.get("/api/events/999/menus")
    assert response.status_code == 404

    # 존재하지 않는 이벤트에 투표 시도
    response = client.post("/api/events/999/votes", json={"menu_id": "1"})
    assert response.status_code == 404

    # 존재하지 않는 이벤트의 결과 조회 시도
    response = client.get("/api/events/999/results")
    assert response.status_code == 404

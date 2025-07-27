# Menu Selection System for Company Gatherings

이 프로젝트는 익명의 참여자들이 특정 회식 이벤트에 대한 메뉴 후보를 제안하고, 투표하며, 그 결과를 확인할 수 있는 FastAPI 기반의 백엔드 시스템입니다.

## 프로젝트 구조

```
menu-selection-backend
├── app
│   ├── api
│   ├── service
│   ├── repository
│   ├── models
│   └── schemas
├── test
├── requirements.txt
└── README.md
```

## 설치 및 실행

1. **가상 환경 생성 및 활성화**
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **필요한 패키지 설치**
   ```
   pip install -r requirements.txt
   ```

3. **애플리케이션 실행**
   ```
   uvicorn app.main:app --reload
   ```

## API 엔드포인트

- **메뉴 목록 조회**: `GET /api/menus`
- **메뉴 추가**: `POST /api/menus`
- **투표하기**: `POST /api/vote`

## 테스트

테스트는 `pytest`를 사용하여 실행합니다. 다음 명령어로 테스트를 실행할 수 있습니다.

```
pytest
```

## 기여

기여를 원하시는 분은 이 저장소를 포크한 후, 변경 사항을 커밋하고 풀 리퀘스트를 제출해 주세요. 

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.
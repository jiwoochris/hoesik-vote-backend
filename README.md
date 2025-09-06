# 회식 메뉴 투표 백엔드

**개요**

익명의 참여자들이 특정 회식 이벤트에 대한 메뉴 후보를 제안하고, 투표하며, 그 결과를 확인할 수 있는 백엔드 API를 구현

- **기능**: 회식 메뉴 투표 이벤트를 생성하고 관리
- **스택**: FastAPI · MongoDB
- **목표**: AI 시대의 개발 문화를 체험하고 GitHub Copilot을 활용하여 실제 실무에 바로 적용하기

## 개발 환경 설정

### MongoDB 설치 및 실행

#### Docker를 사용하는 경우 (권장)

```bash
# 간단한 개발용 (인증 없음)
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

#### 컨테이너 관리

```bash
# 컨테이너 중지
docker stop mongodb

# 컨테이너 시작
docker start mongodb

# 컨테이너 삭제
docker rm mongodb
```

### 애플리케이션 실행

```bash
# 의존성 설치
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest
```

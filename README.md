# 회식 메뉴 투표 백엔드

**개요**

익명의 참여자들이 특정 회식 이벤트에 대한 메뉴 후보를 제안하고, 투표하며, 그 결과를 확인할 수 있는 백엔드 API를 구현

- **기능**: 회식 메뉴 투표 이벤트를 생성하고 관리
- **스택**: FastAPI · MongoDB
- **목표**: AI 시대의 개발 문화를 체험하고 GitHub Copilot을 활용하여 실제 실무에 바로 적용하기

## 개발 환경 설정

### 환경 변수 설정

프로젝트 실행 전에 환경 변수를 설정해야 합니다.

```bash
# .env.example 파일을 복사하여 .env 파일 생성
cp .env.example .env

# 필요에 따라 .env 파일의 설정값을 수정
# 특히 MongoDB 포트 번호나 데이터베이스 이름을 확인하세요
```

`.env` 파일 예시:
```env
# MongoDB 설정
# MongoDB 연결 URI (포트와 데이터베이스 이름 포함)
MONGODB_URI=mongodb://localhost:27017/voting_db
```

### MongoDB 설치 및 실행

#### Docker를 사용하는 경우

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

#### MongoDB 직접 설치

Docker 없이 MongoDB를 직접 설치하려는 경우:

- **Ubuntu (WSL)**: [MongoDB Ubuntu 설치 가이드](https://www.mongodb.com/ko-kr/docs/manual/tutorial/install-mongodb-on-ubuntu/)
- **Windows**: [MongoDB Windows 설치 가이드](https://www.mongodb.com/ko-kr/docs/manual/tutorial/install-mongodb-on-windows/)

### 애플리케이션 실행

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# Linux/MacOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 프로덕션 및 개발 패키지 한 번에 설치
pip install -r requirements.txt -r requirements-dev.txt

# 개발 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API 문서 확인

서버 실행 후 다음 URL에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다:

```
http://localhost:8000/docs
```

### 테스트 실행

```bash
# 가상환경 활성화 (필요시)
# Linux/MacOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 모든 테스트 실행
python -m pytest
```

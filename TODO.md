# TODO

## 현재 작업 상태

### 완료된 작업
- [x] 기본 프로젝트 구조 설정
- [x] FastAPI 기본 설정
- [x] MongoDB 연결 설정
- [x] 이벤트 CRUD 기능 구현
- [x] 메뉴 CRUD 기능 구현
- [x] 투표 기능 구현
- [x] 테스트 환경 설정

### 진행 중인 작업
- [ ] API 문서화 개선
- [ ] 에러 핸들링 개선

### 예정된 작업
- [ ] 인증/권한 시스템 구현
- [ ] 배포 환경 설정
- [ ] CI/CD 파이프라인 구축
- [ ] 로깅 시스템 구현
- [ ] 성능 최적화

## 기술 스택
- FastAPI
- MongoDB
- Pydantic
- pytest

## 아키텍처
레이어드 아키텍처로 구성:
- API Layer (`app/api/`)
- Service Layer (`app/service/`)  
- Repository Layer (`app/repository/`)
- Model Layer (`app/models/`)
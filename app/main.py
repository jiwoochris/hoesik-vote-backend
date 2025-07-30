from fastapi import FastAPI

from app.api.events import router as events_router
from app.database import Base, engine

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
	title="회식 메뉴 투표 API",
	description="익명의 참여자들이 회식 메뉴를 제안하고 투표할 수 있는 API",
	version="1.0.0",
)

# 라우터 등록
app.include_router(events_router)

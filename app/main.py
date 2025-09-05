from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.events import router as events_router
from app.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""애플리케이션 생명주기 관리."""
	# Startup
	await connect_to_mongo()
	yield
	# Shutdown
	await close_mongo_connection()


app = FastAPI(
	title="회식 메뉴 투표 API",
	description="익명의 참여자들이 회식 메뉴를 제안하고 투표할 수 있는 API",
	version="1.0.0",
	lifespan=lifespan,
)

# 라우터 등록
app.include_router(events_router)

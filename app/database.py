from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "voting_db"

client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
	"""MongoDB에 연결합니다."""
	global client, database
	client = AsyncIOMotorClient(MONGODB_URL)
	database = client[DATABASE_NAME]


async def close_mongo_connection():
	"""MongoDB 연결을 닫습니다."""
	global client
	if client:
		client.close()


async def get_database():
	"""MongoDB 데이터베이스 인스턴스를 반환합니다."""
	return database


async def get_db() -> AsyncGenerator:
	"""데이터베이스를 제공하는 의존성."""
	db = await get_database()
	try:
		yield db
	finally:
		pass  # MongoDB는 자동으로 연결을 관리합니다

from collections.abc import AsyncGenerator
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings


class DatabaseManager:
    """MongoDB 연결 관리 클래스."""
    
    def __init__(self):
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """MongoDB에 연결합니다."""
        if self._client is None:
            self._client = AsyncIOMotorClient(settings.mongodb_uri)
            # URI에서 데이터베이스 이름 추출
            database_name = settings.mongodb_uri.split('/')[-1] if '/' in settings.mongodb_uri else 'voting_db'
            self._database = self._client[database_name]
    
    async def disconnect(self):
        """MongoDB 연결을 닫습니다."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None
    
    def get_database(self) -> AsyncIOMotorDatabase:
        """데이터베이스 인스턴스를 반환합니다."""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database


# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()


async def connect_to_mongo():
    """MongoDB에 연결합니다."""
    await db_manager.connect()


async def close_mongo_connection():
    """MongoDB 연결을 닫습니다."""
    await db_manager.disconnect()


async def get_database():
    """MongoDB 데이터베이스 인스턴스를 반환합니다."""
    return db_manager.get_database()


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """데이터베이스를 제공하는 의존성."""
    db = db_manager.get_database()
    try:
        yield db
    finally:
        pass  # MongoDB는 자동으로 연결을 관리합니다

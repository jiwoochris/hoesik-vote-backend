"""애플리케이션 설정 관리 모듈."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정 클래스."""
    
    # MongoDB 설정
    mongodb_uri: str = Field(
        default="mongodb://localhost:27017/voting_db",
        description="MongoDB 연결 URI (데이터베이스 이름 포함)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# 전역 설정 인스턴스
settings = Settings()

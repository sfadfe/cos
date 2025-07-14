from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    JWT_SECRET_KEY: str  # JWT 비밀 키
    JWT_ACCESS_EXPIRES_IN_HOURS: float  # JWT 액세스 토큰 만료 시간 (시간 단위)]
    JWT_ALGORITHM: str = "HS256"  # JWT 알고리즘

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()  # type: ignore
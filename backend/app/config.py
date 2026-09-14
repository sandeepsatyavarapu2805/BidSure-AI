from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    app_name: str = "BidSure AI"
    environment: str = "development"

    database_url: str

    app_secret: str
    session_cookie_name: str = "bidsure_session"
    session_ttl_hours: int = 12

    frontend_origin: str = "http://localhost:5173"

    storage_root: Path = PROJECT_ROOT / "data" / "storage"
    max_upload_mb: int = 25

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

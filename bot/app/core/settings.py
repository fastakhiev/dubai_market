from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN")
    ADMIN_TELEGRAM_TOKEN: str = os.environ.get("ADMIN_TELEGRAM_TOKEN")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST")
    ELASTIC_PORT: int = os.getenv("ELASTIC_PORT")
    FILES_BUCKET_URL: str = os.getenv("FILES_BUCKET_URL")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    ADMIN_TELEGRAM_IDS: list[int] = list(map(int, os.getenv("ADMIN_TELEGRAM_IDS", "").split(",")))


@lru_cache()
def get_settings() -> Settings:
    return Settings()

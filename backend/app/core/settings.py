from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_PORT: int = os.getenv("MINIO_PORT")
    MINIO_HOST: str = os.getenv("MINIO_HOST")
    MINIO_BUCKET_PREVIEW: str = os.getenv("MINIO_BUCKET_PREVIEW")
    MINIO_BUCKET_PASSPORT: str = os.getenv("MINIO_BUCKET_PASSPORT")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
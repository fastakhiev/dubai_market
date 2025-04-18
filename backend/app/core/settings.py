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


@lru_cache()
def get_settings() -> Settings:
    return Settings()
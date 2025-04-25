from minio import Minio
from app.core import config

minio_client = Minio(
    f"{config.MINIO_HOST}:{config.MINIO_PORT}",
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False
)

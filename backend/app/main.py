from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.db import database
from app.core.http_client import get_http_session, close_http_session
from app.core.minio_client import minio_client
from app.core import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()
    await get_http_session()
    minio_client.make_bucket(config.MINIO_BUCKET_PREVIEW) if not minio_client.bucket_exists(config.MINIO_BUCKET_PREVIEW) else None
    print("start")


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
    await close_http_session()
    print("stop")


app.include_router(router)

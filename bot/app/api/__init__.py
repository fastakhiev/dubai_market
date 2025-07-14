from fastapi import APIRouter
from app.api.v1.routes import router as ban_router

router = APIRouter()

router.include_router(ban_router)

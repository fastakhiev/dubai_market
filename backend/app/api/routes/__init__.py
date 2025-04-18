from fastapi import APIRouter
from app.api.routes.v1.routes import router as image_router

router = APIRouter()
router.include_router(image_router)

from aiogram import Router
from app.handlers.v1.search import router as search_router
from app.handlers.v1.admin import router as admin_router
from app.handlers.v1.common import router as common_router

router = Router()

router.include_router(admin_router)
router.include_router(search_router)
router.include_router(common_router)

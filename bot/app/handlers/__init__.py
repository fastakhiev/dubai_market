from aiogram import Router
from app.handlers.v1.sign_up import router as sign_up_router
from app.handlers.v1.sellers import router as sellers_router
from app.handlers.v1.search import router as search_router
from app.handlers.v1.buyers import router as buyers_router
from app.handlers.v1.common import router as common_router
from app.handlers.v1.commands import router as commands_router

router = Router()
router.include_router(sign_up_router)
router.include_router(sellers_router)
router.include_router(search_router)
router.include_router(buyers_router)
router.include_router(common_router)
router.include_router(commands_router)

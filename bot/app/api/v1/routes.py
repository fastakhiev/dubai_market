from fastapi import APIRouter, Response
from app.schemas.schemas import BanUser
from app.core.ban_cache import ban_cache

router = APIRouter()

@router.post("/ban_user")
async def ban_user(data: BanUser):
    ban_cache.pop(data.telegram_id, None)
    return Response(status_code=200, content="ok")

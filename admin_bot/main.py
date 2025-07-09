import asyncio
from aiogram import Dispatcher
from app.core.db import database
from app.core.bot import bot
from app.middlewares.access_middleware import AdminAccessMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from app.core import config
from app.handlers import router

storage = RedisStorage.from_url(f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")
dp = Dispatcher(storage=storage)

async def main():
    dp.include_router(router)
    dp.message.middleware(AdminAccessMiddleware(allowed_ids=config.TELEGRAM_IDS))
    await database.connect()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
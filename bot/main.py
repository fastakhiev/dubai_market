import asyncio
from aiogram import Dispatcher
from app.handlers import router
from app.core.db import database
from app.core.bot import bot
from app.middlewares.error_middleware import ErrorMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from app.core import config


storage = RedisStorage.from_url(f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(router)
    dp.update.middleware(ErrorMiddleware())
    await database.connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

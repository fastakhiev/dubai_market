import asyncio
from aiogram import Dispatcher
from app.handlers import router
from app.core.db import database
from app.core.bot import bot
from app.handlers.v1.errors import router as error_router
from aiogram.fsm.storage.redis import RedisStorage


storage = RedisStorage.from_url("redis://redis:6379")
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(router)
    dp.errors.register(error_router)
    await database.connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

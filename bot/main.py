import asyncio
import uvicorn
from aiogram import Dispatcher, types
from app.handlers import router
from app.core.db import database
from app.core.bot import bot
from app.middlewares.error_middleware import ErrorMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from app.core import config
from fastapi import FastAPI
from app.api import router as fastapi_router
from app.middlewares.ban_middleware import BanMiddleware


storage = RedisStorage.from_url(f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")
dp = Dispatcher(storage=storage)
app = FastAPI()
app.include_router(fastapi_router)


@app.on_event("startup")
async def on_startup():
    router.message.middleware(BanMiddleware())
    dp.include_router(router)
    dp.update.middleware(ErrorMiddleware())
    await database.connect()
    asyncio.create_task(dp.start_polling(bot))

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()
    await bot.session.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
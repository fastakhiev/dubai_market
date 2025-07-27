from aiogram import Bot
from app.core import config

admin_bot = Bot(token=config.ADMIN_TELEGRAM_TOKEN)

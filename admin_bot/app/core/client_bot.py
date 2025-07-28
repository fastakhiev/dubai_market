from aiogram import Bot
from app.core import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

client_bot = Bot(token=config.CLIENT_TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

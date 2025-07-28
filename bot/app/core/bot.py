from aiogram import Bot
from app.core import config
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=config.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

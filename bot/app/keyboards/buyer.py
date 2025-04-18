from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

buyer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поиск", switch_inline_query_current_chat="")]
    ]
)

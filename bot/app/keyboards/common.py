from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

search_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поиск", switch_inline_query_current_chat="")]
    ]
)

notification_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Окей", callback_data="delete_notification")]
    ]
)

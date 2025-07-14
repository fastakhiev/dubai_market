from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

notification_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Окей", callback_data="delete_notification")]
    ]
)
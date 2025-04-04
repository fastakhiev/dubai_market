from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Покупатель', callback_data="buyer")],
    [InlineKeyboardButton(text='Продавец', callback_data="seller")]
])
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


seller = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мой магазин"), KeyboardButton(text="Мои товары")],
        [KeyboardButton(text="Вопросы"), KeyboardButton(text="Создать товар")],
        [KeyboardButton(text="Заказы")],
    ],
    resize_keyboard=True,
)

currency = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="RUB", callback_data="RUB")],
        [InlineKeyboardButton(text="AED", callback_data="AED")],
        [InlineKeyboardButton(text="USD", callback_data="USD")],
    ]
)

cancel_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад")]], resize_keyboard=True
)

currency_list = ["RUB", "AED", "USD"]

categories_general = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Электроника", callback_data="Электроника")],
        [InlineKeyboardButton(text="Бытовая техника", callback_data="Бытовая техника")],
        [InlineKeyboardButton(text="Авто и мото", callback_data="Авто и мото")],
        [
            InlineKeyboardButton(
                text="Одежда, обувь и аксессуары",
                callback_data="Одежда, обувь и аксессуары",
            )
        ],
        [
            InlineKeyboardButton(
                text="Красота и здоровье", callback_data="Красота и здоровье"
            )
        ],
        [InlineKeyboardButton(text="Дом и сад", callback_data="Дом и сад")],
        [InlineKeyboardButton(text="Детские товары", callback_data="Детские товары")],
        [
            InlineKeyboardButton(
                text="Хобби и развлечения", callback_data="Хобби и развлечения"
            )
        ],
        [
            InlineKeyboardButton(
                text="Спорт и активный отдых", callback_data="Спорт и активный отдых"
            )
        ],
        [InlineKeyboardButton(text="Животные", callback_data="Животные")],
        [InlineKeyboardButton(text="Услуги", callback_data="Услуги")],
    ]
)

categories_list = [
    "Электроника",
    "Бытовая техника",
    "Авто и мото",
    "Одежда, обувь и аксессуары",
    "Красота и здоровье",
    "Дом и сад",
    "Детские товары",
    "Хобби и развлечения",
    "Спорт и активный отдых",
    "Животные",
    "Услуги",
]


def generate_pagination_buttons(page: int, total_pages: int, user_id: str):
    buttons = []
    if page + 1 - total_pages == 0 and page == 0:
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    if page + 1 > 1:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Назад", callback_data=f"prev_page:{user_id}:{page - 1}"
                )
            ]
        )

    if page + 1 < total_pages:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперёд", callback_data=f"next_page:{user_id}:{page + 1}"
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)

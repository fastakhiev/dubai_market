from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


seller = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мой магазин", callback_data="my_shop")],
        [InlineKeyboardButton(text="Мои товары", callback_data="my_products")],
        [InlineKeyboardButton(text="Вопросы", callback_data="questions_seller")],
        [InlineKeyboardButton(text="Создать товар", callback_data="create_product")],
        [InlineKeyboardButton(text="Заказы", callback_data="orders_seller")]
    ]
)

inline_back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
)

my_products = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поиск", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
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

product_inline_buttons_seller = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_from_product_seller")]
    ]
)

order_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="approve_order")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_order_seller")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
)

question_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data="answer_question")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
)

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

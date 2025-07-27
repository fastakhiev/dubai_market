from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

buyer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к поиску", callback_data="search_buyer")],
        [InlineKeyboardButton(text="Заказы", callback_data="orders_buyer")],
        [InlineKeyboardButton(text="Вопросы", callback_data="questions_buyer")]
    ]
)


search_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к поиску", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_search")],
    ]
)

orders_list_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="Назад", callback_data="back_buyer")]
    ]
)

inline_back_buyer_from_order = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_from_order_buyer")]
    ]
)

reply_back_buyer = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить")]
    ],
    resize_keyboard=True
)

product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить товар", callback_data="buy_product")],
        [InlineKeyboardButton(text="Продавец", callback_data="get_seller_from_product")],
        [InlineKeyboardButton(text="Задать вопрос", callback_data="ask_product")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_product", switch_inline_query_current_chat="")]
    ]
)

back_from_shop_buyer_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_from_shop_buyer")]
    ]
)

my_product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_from_product", switch_inline_query_current_chat="")]
    ]
)

search_filters = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поиск без фильтра", callback_data="without_filter")],
        [InlineKeyboardButton(text="Электроника", callback_data="Электроника_b")],
        [InlineKeyboardButton(text="Бытовая техника", callback_data="Бытовая техника_b")],
        [InlineKeyboardButton(text="Авто и мото", callback_data="Авто и мото_b")],
        [
            InlineKeyboardButton(
                text="Одежда, обувь и аксессуары",
                callback_data="Одежда, обувь и аксессуары_b",
            )
        ],
        [
            InlineKeyboardButton(
                text="Красота и здоровье", callback_data="Красота и здоровье_b"
            )
        ],
        [InlineKeyboardButton(text="Дом и сад", callback_data="Дом и сад_b")],
        [InlineKeyboardButton(text="Детские товары", callback_data="Детские товары_b")],
        [
            InlineKeyboardButton(
                text="Хобби и развлечения", callback_data="Хобби и развлечения_b"
            )
        ],
        [
            InlineKeyboardButton(
                text="Спорт и активный отдых", callback_data="Спорт и активный отдых_b"
            )
        ],
        [InlineKeyboardButton(text="Животные", callback_data="Животные_b")],
        [InlineKeyboardButton(text="Услуги", callback_data="Услуги_b")],
        [InlineKeyboardButton(text="Назад", callback_data="back_buyer")]
    ]
)

categories_list_b = [
    "Электроника_b",
    "Бытовая техника_b",
    "Авто и мото_b",
    "Одежда, обувь и аксессуары_b",
    "Красота и здоровье_b",
    "Дом и сад_b",
    "Детские товары_b",
    "Хобби и развлечения_b",
    "Спорт и активный отдых_b",
    "Животные_b",
    "Услуги_b",
]


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


basic = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Профили продавцов", callback_data="shops")],
        [InlineKeyboardButton(text="Статистика", callback_data="statistics")],
        [InlineKeyboardButton(text="Товары", callback_data="products")],
        [InlineKeyboardButton(text="Товары на проверке", callback_data="moderation_products")],
        [InlineKeyboardButton(text="Паспорта на проверке", callback_data="moderation_passports")]
    ]
)

search_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к поиску", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_search")]
    ]
)

shop_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Владелец", callback_data="shop_owner_from_shop")],
        [InlineKeyboardButton(text="Товары", callback_data="products_from_shop")],
        [InlineKeyboardButton(text="Забанить", callback_data="block_from_shop")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_shop")]
    ]
)

blocked_shop_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Владелец", callback_data="shop_owner_from_shop")],
        [InlineKeyboardButton(text="Товары", callback_data="products_from_shop")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_shop")]
    ]
)

product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Магазин", callback_data="shop_from_product")],
        [InlineKeyboardButton(text="Забанить", callback_data="block_from_product")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_product")]
    ]
)

blocked_product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Магазин", callback_data="shop_from_product")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_product")]
    ]
)

seller_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Забанить", callback_data="block_from_seller")],
        [InlineKeyboardButton(text="На главную", callback_data="back_from_seller")]
    ]
)

blocked_seller_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="На главную", callback_data="back_from_seller")]
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
        [InlineKeyboardButton(text="На главную", callback_data="back_from_search_products")]
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

approve_block_shop_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="approve_block_shop")],
        [InlineKeyboardButton(text="Нет", callback_data="not_approve_block_shop")]
    ]
)

approve_block_seller_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="approve_block_seller")],
        [InlineKeyboardButton(text="Нет", callback_data="not_approve_block_seller")]
    ]
)

approve_block_product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="approve_block_product")],
        [InlineKeyboardButton(text="Нет", callback_data="not_approve_block_product")]
    ]
)

statistics_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_from_statics")]
    ]
)

moderation_product_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отклонить", callback_data="reject_moderation_products")],
        [InlineKeyboardButton(text="Одобрить", callback_data="approve_moderation_products")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_moderation_product")]
    ]
)

moderation_passport_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отклонить", callback_data="reject_moderation_passports")],
        [InlineKeyboardButton(text="Одобрить", callback_data="approve_moderation_passports")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_moderation_passport")]
    ]
)

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.basic import basic, search_buttons, seller_buttons, categories_list_b, search_filters, shop_buttons, approve_block_shop_buttons, approve_block_seller_buttons, blocked_shop_buttons, blocked_seller_buttons, approve_block_product_buttons, statistics_buttons
from app.states.states import SearchFilter, CurrentShop, CurrentOwner, RejectProduct, RejectPassport, ApproveProduct
from app.models.shops import Shop
from uuid import UUID
from app.models.products import Product
from app.models.users import User
from app.core.elastic import es
from app.core.bot import bot
from collections import defaultdict
from app.core.client_bot import client_bot
from app.keyboards.clients import notification_button
import httpx
from app.core import config


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Действия", reply_markup=basic)


@router.callback_query(F.data == "shops")
async def selected_shops(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Поиск по магазинам", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="shops")
    await callback.answer()


@router.callback_query(F.data == "products")
async def go_to_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выбирете фильтр", reply_markup=search_filters)


@router.callback_query(F.data == "without_filter")
async def search_without_filter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Поиск без фильтра", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="products")


@router.callback_query(lambda c: c.data in categories_list_b)
async def search_with_filter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text(f"<strong>Поиск по:</strong> {callback.data[:-2]}", reply_markup=search_buttons)
    await state.update_data(filter={"category": callback.data[:-2]}, message={
        "message_id": message.message_id
    }, type="products")
    await callback.answer()



@router.callback_query(F.data == "back_from_search")
async def back_from_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "back_from_search_products")
async def back_from_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "back_from_shop")
async def back_from_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "shop_owner_from_shop")
async def get_shop_owner(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    current_shop = await state.get_data()
    shop = await Shop.objects.select_related("user_id").get(id=UUID(current_shop["current_shop"]["shop_id"]))
    await state.clear()
    await state.set_state(CurrentOwner.current_owner)
    await state.update_data(current_owner={
        "id": str(shop.user_id.id),
        "name": shop.user_id.full_name,
    })
    await callback.message.answer_photo(
        photo=f"https://dubaimarketbot.ru/get_image/{shop.user_id.passport}",
        caption=f"<strong>Имя:</strong> {shop.user_id.full_name}\n<strong>Телефон:</strong> {shop.user_id.phone}\n<strong>Дата регистрации:</strong> {shop.user_id.created_at}\n<strong>Passport:</strong> {shop.user_id.passport}\n<strong>Статус:</strong> {'активен' if shop.user_id.is_active else 'забанен'}",
        reply_markup=seller_buttons if shop.user_id.is_active else blocked_seller_buttons)
    await callback.answer()


@router.callback_query(F.data == "back_from_seller")
async def back_from_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "shop_from_product")
async def shop_from_product (callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)
    product = await Product.objects.get(id=UUID(data["current_product"]["product_id"]))
    shop = await Shop.objects.get(user_id=product.seller_id)
    await state.clear()
    messages_ids = []
    await state.set_state(CurrentShop.current_shop)
    send_photos = await callback.message.answer_photo(
        photo=f"https://dubaimarketbot.ru/get_image/{shop.photo}",
        caption=f"<strong>Название:</strong> {shop.name}\n<strong>Социальные сети:</strong> {shop.social_networks}\n<strong>Статус:</strong> {'активен' if shop.is_active else 'забанен'}",
        reply_markup=shop_buttons if shop.is_active else blocked_shop_buttons
    )
    messages_ids.append(send_photos.message_id)
    await state.update_data(current_shop={
        "messages_ids": messages_ids,
        "chat_id": callback.message.chat.id,
        "shop_id": str(shop.id),
        "shop_name": shop.name,
        "seller_id": str(product.seller_id.id)
    })
    await callback.answer()


@router.callback_query(F.data == "products_from_shop")
async def go_to_search(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    await callback.message.delete()
    message = await callback.message.answer(f"<strong>Поиск по:</strong> {data['current_shop']['shop_name']}", reply_markup=search_buttons)
    await state.update_data(filter={"seller_id": data["current_shop"]["seller_id"]}, message={
        "message_id": message.message_id
    }, type="products")
    await callback.answer()


@router.callback_query(F.data == "block_from_shop")
async def block_from_shop(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Вы уверены, что хотите заблокировать магазин?\nПосле блокировки товары также будут заблокированы", reply_markup=approve_block_shop_buttons)


@router.callback_query(F.data == "approve_block_shop")
async def approve_block_shop(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    products = await Product.objects.filter(seller_id=UUID(data["current_shop"]["seller_id"])).all()
    for i in products:
        i.is_active = False
        await i.update()
        await es.update(
            index="products",
            id=str(i.id),
            body={
                "doc" : {
                    "is_active": False
                }
            }
        )
    shop = await Shop.objects.select_related("user_id").get(id=UUID(data["current_shop"]["shop_id"]))
    shop.is_active = False
    await es.update(
        index="shops",
        id=data["current_shop"]["shop_id"],
        body={
            "doc": {
                "is_active": False
            }
        }
    )
    await shop.update()
    await client_bot.send_message(
        chat_id=shop.user_id.telegram_id,
        text=f"Ваш магазин {shop.name} и его товары были заблокированы администратором",
        reply_markup=notification_button
    )
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f"Вы заблокировали магазин {data['current_shop']['shop_name']} и его товары\nВыберите действия", reply_markup=basic)


@router.callback_query(F.data == "not_approve_block_shop")
async def not_approve_block_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer("Вы отменили отказались от блокировки магазина\nВыберите действия", reply_markup=basic)


@router.callback_query(F.data == "back_from_product")
async def back_from_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)
    await state.clear()
    await callback.answer()
    await callback.message.answer("Действия", reply_markup=basic)


@router.callback_query(F.data == "block_from_seller")
async def block_from_seller(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    await callback.message.answer(
        text=f"Вы уверены что хотите заблокировать этого продавца {data['current_owner']['name']}, вместе с ним будет заблокирован магазин и его товары",
        reply_markup=approve_block_seller_buttons
    )
    await callback.answer()


@router.callback_query(F.data == "approve_block_seller")
async def approve_block_seller(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    products = await Product.objects.filter(seller_id=UUID(data["current_owner"]["id"])).all()
    for i in products:
        i.is_active = False
        await i.update()
        await es.update(
            index="products",
            id=str(i.id),
            body={
                "doc": {
                    "is_active": False
                }
            }
        )

    shop = await Shop.objects.get(user_id=UUID(data["current_owner"]["id"]))
    shop.is_active = False
    await es.update(
        index="shops",
        id=str(shop.id),
        body={
            "doc": {
                "is_active": False
            }
        }
    )
    await shop.update()
    seller = await User.objects.get(id=UUID(data["current_owner"]["id"]))
    seller.is_active = False
    seller_tg_id = seller.telegram_id
    await seller.update()
    httpx.post(
        f"http://{config.CLIENT_BOT_HOST}:{config.CLIENT_BOT_PORT}/ban_user",
        json={
            "telegram_id": seller_tg_id
        }
    )
    await client_bot.send_message(
        chat_id=seller_tg_id,
        text=f"Вы и ваш магазин с товарами были заблокированы администратором",
    )
    await state.clear()
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(f"Вы заблокировали продавца {data['current_owner']['name']} его магазин и товары\nВыберите действия", reply_markup=basic)


@router.callback_query(F.data == "not_approve_block_seller")
async def not_approve_block_seller(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("Вы отменили отказались от блокировки продавца\nВыберите действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "block_from_product")
async def block_from_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)
    await callback.message.answer("Вы уверены что хотите забанить товар?", reply_markup=approve_block_product_buttons)
    await callback.answer()


@router.callback_query(F.data == "not_approve_block_product")
async def not_approve_block_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("Вы отменили отказались от блокировки товара\nВыберите действия",
                                  reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "approve_block_product")
async def approve_block_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.delete()
    product = await Product.objects.select_related('seller_id').get(id=UUID(data["current_product"]["product_id"]))
    product.is_active = False
    await product.update()
    await es.update(
        index="products",
        id=str(product.id),
        body={
            "doc": {
                "is_active": False
            }
        }
    )
    await client_bot.send_message(
        chat_id=product.seller_id.telegram_id,
        text=f"Ваш товар {product.title} был заблокирован администратором",
        reply_markup=notification_button
    )
    await state.clear()
    await callback.answer()
    await callback.message.answer(f"Вы заблокировали товар\nВыберите действия", reply_markup=basic)


@router.callback_query(F.data == "statistics")
async def get_statistics(callback: CallbackQuery):
    count_users = await User.objects.count()
    products = await Product.objects.all()

    stats = defaultdict(lambda: {"active": 0, "inactive": 0})

    for product in products:
        if product.is_active:
            stats[product.category]["active"] += 1
        else:
            stats[product.category]["inactive"] += 1

    result_products = "\n".join(
        f"<strong>{category}:</strong> активных={counts['active']}, неактивных={counts['inactive']}"
        for category, counts in stats.items()
    )
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(
        text=f"<strong>Количество продавцов и  покупателей:</strong> {count_users}\n{result_products}",
        reply_markup=statistics_buttons
    )


@router.callback_query(F.data == "back_from_statics")
async def back_from_statics(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "moderation_products")
async def get_moderation_products(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Товары на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="moderation_products")
    await callback.answer()


@router.callback_query(F.data == "back_from_moderation_product")
async def back_from_moderation_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.answer("Товары на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
            "message_id": message.message_id
        }, type="moderation_products")
    await callback.answer()


@router.callback_query(F.data == "approve_moderation_products")
async def approve_moderation_products(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)

    product = await Product.objects.select_related("seller_id").get(id=UUID(data["current_product"]["product_id"]))
    product.is_moderation = False
    product.is_active = True
    await product.update()
    await es.update(
        index="products",
        id=str(product.id),
        body={
            "doc": {
                "is_moderation": False,
                "is_active": True
            }
        }
    )
    await state.set_state(ApproveProduct.telegram_id)
    await state.update_data(telegram_id=product.seller_id.telegram_id)
    await state.set_state(ApproveProduct.problem_approve_product)
    await callback.message.answer("Введите комментарий")
    await callback.answer()


@router.message(ApproveProduct.problem_approve_product)
async def enter_problem_product(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await client_bot.send_message(chat_id=str(data["telegram_id"]),
                                  text=f"Ваш товар прошел проверку\n<strong>Комментарий:</strong> {message.text}")
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await message.answer("Вы отклонили товар\nТовары на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="moderation_products")


@router.callback_query(F.data == "reject_moderation_products")
async def reject_moderation_products(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_product"]["chat_id"], message_id=i)

    product = await Product.objects.select_related("seller_id").get(id=UUID(data["current_product"]["product_id"]))
    product.is_moderation = False
    product.is_active = False
    await product.update()
    await es.update(
        index="products",
        id=str(product.id),
        body={
            "doc": {
                "is_moderation": False,
                "is_active": False
            }
        }
    )
    await state.set_state(RejectProduct.telegram_id)
    await state.update_data(telegram_id=product.seller_id.telegram_id)
    await state.set_state(RejectProduct.problem_product)
    await callback.message.answer("Введите причину отказа")
    await callback.answer()


@router.message(RejectProduct.problem_product)
async def enter_problem_product(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await client_bot.send_message(chat_id=str(data["telegram_id"]),
                                  text=f"Ваш товар не прошел проверку\n<strong>Причина:</strong> {message.text}")
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await message.answer("Вы отклонили товар\nТовары на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="moderation_products")


@router.callback_query(F.data == "moderation_passports")
async def get_moderation_products(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Паспорта на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="moderation_passports")
    await callback.answer()


@router.callback_query(F.data == "back_from_moderation_passport")
async def back_from_moderation_passport(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_shop"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_shop"]["chat_id"], message_id=i)
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.answer("Паспорта на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
            "message_id": message.message_id
        }, type="moderation_passports")
    await callback.answer()


@router.callback_query(F.data == "approve_moderation_passports")
async def approve_moderation_passports(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_shop"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_shop"]["chat_id"], message_id=i)

    shop = await Shop.objects.select_related("user_id").get(id=UUID(data["current_shop"]["shop_id"]))
    shop.is_moderation = False
    shop.is_verified = True
    await shop.update()
    await es.update(
        index="shops",
        id=str(shop.id),
        body={
            "doc": {
                "is_moderation": False,
                "is_verified": True
            }
        }
    )
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.answer("Вы одобрили паспорт\nПаспорта на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
            "message_id": message.message_id
        }, type="moderation_passports")
    await client_bot.send_message(chat_id=str(shop.user_id.telegram_id), text=f"Ваш паспорт прошел проверку")
    await callback.answer()


@router.callback_query(F.data == "reject_moderation_passports")
async def reject_moderation_products(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    for i in data["current_shop"]["messages_ids"]:
        await bot.delete_message(chat_id=data["current_shop"]["chat_id"], message_id=i)

    shop = await Shop.objects.select_related("user_id").get(id=UUID(data["current_shop"]["shop_id"]))
    shop.is_moderation = False
    shop.is_verified = False
    await shop.update()
    await es.update(
        index="shops",
        id=str(shop.id),
        body={
            "doc": {
                "is_moderation": False,
                "is_verified": False
            }
        }
    )
    await state.set_state(RejectPassport.telegram_id)
    await state.update_data(telegram_id=shop.user_id.telegram_id)
    await state.set_state(RejectPassport.problem_passport)
    await callback.message.answer("Введите причину отказа")
    await callback.answer()


@router.message(RejectPassport.problem_passport)
async def enter_problem_passport(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await client_bot.send_message(chat_id=str(data["telegram_id"]),
                                  text=f"Ваш паспорт не прошел проверку\n<strong>Причина:</strong> {message.text}")
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await message.answer("Вы отклонили паспорт\nПаспорта на модерации", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="moderation_passports")

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.basic import basic, search_buttons, seller_buttons, categories_list_b, search_filters, shop_buttons, approve_block_shop_buttons
from app.states.states import SearchFilter, CurrentShop
from app.models.shops import Shop
from uuid import UUID
from app.models.products import Product
from app.core.elastic import es

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
    message = await callback.message.edit_text(f"Поиск по {callback.data[:-2]}", reply_markup=search_buttons)
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
    await callback.message.answer(f"Имя: {shop.user_id.full_name}\nТелефон: {shop.user_id.phone}\nДата регистрации: {shop.user_id.created_at}\nPassport: {shop.user_id.passport}", reply_markup=seller_buttons)
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
    product = await Product.objects.get(id=UUID(data["current_product"]["product_id"]))
    shop = await Shop.objects.get(user_id=product.seller_id)
    await state.clear()
    await callback.message.delete()
    messages_ids = []
    await state.set_state(CurrentShop.current_shop)
    send_photos = await callback.message.answer_photo(
        photo=f"https://images.steamusercontent.com/ugc/52453354080448818/543783B601D5A853E3F50907B9722A314DFD92B6/?imw=512&amp;imh=320&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true",
        caption=f"Название: {shop.name}\nСоциальные сети: {shop.social_networks}\n ",
        reply_markup=shop_buttons
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
    message = await callback.message.answer(f"Поиск по {data['current_shop']['shop_name']}", reply_markup=search_buttons)
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
    shop = await Shop.objects.get(id=UUID(data["current_shop"]["shop_id"]))
    shop.is_active = False
    await es.update(
        index="products",
        id=data["current_shop"]["shop_id"],
        body={
            "doc": {
                "is_active": False
            }
        }
    )
    await shop.update()
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f"Вы заблокировали магазин {data['current_shop']['shop_name']} и его товары\nВыберите действия", reply_markup=basic)


@router.callback_query(F.data == "not_approve_block_shop")
async def not_approve_block_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Вы отменили отказались от блокировки магазина\nВыберите действия", reply_markup=basic)
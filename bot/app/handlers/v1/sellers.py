from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from uuid import UUID

from app.models.shops import Shop
from app.models.products import Product
from app.models.users import User
from app.keyboards.seller import currency, my_products
from app.core.bot import bot
from app.states.states import CreateProduct, SearchFilter
from app.handlers.utils.get_user_products import get_user_products
from app.middlewares.album_middleware import AlbumMiddleware
from app.core.elastic import es
from app.keyboards.seller import (
    categories_general,
    categories_list,
    currency_list,
    cancel_button,
    seller as seller_kb,
    inline_back_button
)


router = Router()
router.message.middleware(AlbumMiddleware())


@router.callback_query(F.data == "my_shop")
async def get_my_shop(callback: CallbackQuery):
    shop = await Shop.objects.select_related("user_id").get(
        user_id__telegram_id=str(callback.from_user.id)
    )
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=shop.photo,
            caption=f"Название: {shop.name}\nСоциальные сети: {shop.social_networks}\n "
        ),
        reply_markup=inline_back_button
    )
    await callback.answer()


@router.callback_query(F.data == "my_products")
async def get_my_products(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(SearchFilter.filter)
    await state.set_state(SearchFilter.message)
    user = await User.objects.get(telegram_id=str(callback.from_user.id))
    message = await callback.message.edit_text("Нажмите для вывода", reply_markup=my_products)
    await state.update_data(filter={"seller_id": str(user.id)}, message={
        "type": "seller",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "back_from_product_seller")
async def back_from_product_sel(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for i in state_data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=state_data["current_product"]["chat_id"], message_id=i)

    message = await callback.message.answer("Нажмите для вывода", reply_markup=my_products)
    await state.update_data(filter=state_data["filter"], message={
        "type": "seller",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "back")
async def back_seller(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Выбирете действие",
        reply_markup=seller_kb
    )
    await state.clear()
    await callback.answer()


@router.message(F.text == "Назад")
async def cancel_create_product(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы отменили создание товара", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выбрете действие", reply_markup=seller_kb)


@router.callback_query(F.data == "create_product")
async def create_product(callbck: CallbackQuery, state: FSMContext):
    user = await User.objects.get(telegram_id=str(callbck.from_user.id))
    await state.set_state(CreateProduct.seller_id)
    await state.update_data(seller_id=str(user.id))
    await state.set_state(CreateProduct.title)
    await callbck.message.delete()
    await callbck.answer()
    await callbck.message.answer("Введите название товара", reply_markup=cancel_button)


@router.message(CreateProduct.title)
async def create_product_enter_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(CreateProduct.description)
    await message.answer("Введите описание товара")


@router.message(CreateProduct.description)
async def create_product_enter_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateProduct.price)
    await message.answer("Ведите стоимость товара")


@router.message(CreateProduct.price)
async def create_product_enter_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(CreateProduct.currency)
    await message.answer("Выберете валюту", reply_markup=currency)


@router.callback_query(lambda c: c.data in currency_list)
async def create_product_enter_currency(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(currency=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(CreateProduct.photos)
    await callback.message.answer("Загрузите до 10 фото одним сообщением")


@router.message(CreateProduct.photos)
async def create_product_upload_photos(
    message: Message, state: FSMContext, album: list = None
):
    if album:
        photos = [msg.photo[-1].file_id for msg in album]
        photos.append(album[0].photo[0].file_id)
    else:
        if not message.photo:
            await message.answer("Пожалуйста, отправьте фото.")
            return
        photos = [message.photo[-1].file_id, message.photo[0].file_id]

    if len(photos) > 10:
        await message.answer("Вы можете загрузить не более 10 фото!")
        return

    await state.update_data(photos=photos)
    await message.answer(f"✅ Вы загрузили {len(photos)} фото.")
    await state.set_state(CreateProduct.category)
    await message.answer("Выберете категорию товара", reply_markup=categories_general)


@router.callback_query(lambda c: c.data in categories_list)
async def create_product_enter_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data)
    data = await state.get_data()
    data["seller_id"] = UUID(data["seller_id"])
    thumbnail = data["photos"].pop(-1)

    product = await Product.objects.create(
        title=data["title"],
        description=data["description"],
        price=data["price"],
        currency=data["currency"],
        seller_id=data["seller_id"],
        status="active",
        photos=list(data["photos"]),
        thumbnail=thumbnail,
        category=data["category"],
    )
    product_dict = product.model_dump()
    product_dict["id"] = str(product_dict["id"])
    product_dict["seller_id"] = str(product.seller_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(f"Вы выбрали {callback.data}")
    await es.index(index="products", id=product_dict["id"], body={
        "id": str(product.id),
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "currency": product.currency,
        "seller_id": str(product.seller_id),
        "status": product.status,
        "thumbnail": product.thumbnail,
        "category": product.category
    })
    await callback.message.answer("Товар создан", reply_markup=seller_kb)


@router.callback_query(F.data == "orders_seller")
async def get_orders_seller(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.filter)
    await state.set_state(SearchFilter.message)
    message = await callback.message.answer("Нажмите для вывода", reply_markup=my_products)
    await state.update_data(filter={"orders": str(callback.from_user.id)}, message={
        "type": "seller",
        "message_id": message.message_id
    })
    await callback.answer()

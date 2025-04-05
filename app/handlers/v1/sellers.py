from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from uuid import UUID

from app.models.shops import Shop
from app.models.products import Product
from app.models.users import User
from app.keyboards.seller import currency
from app.core.bot import bot
from app.states.states import CreateProduct, MyProducts
from app.handlers.utils.get_user_products import get_user_products
from app.middlewares.album_middleware import AlbumMiddleware
from app.core.elastic import es
from app.keyboards.seller import (
    categories_general,
    categories_list,
    currency_list,
    cancel_button,
    generate_pagination_buttons,
    seller as seller_kb,
)

router = Router()
router.message.middleware(AlbumMiddleware())


@router.message(F.text == "Мой магазин")
async def get_my_shop(message: Message):
    shop = await Shop.objects.select_related("user_id").get(
        user_id__telegram_id=str(message.from_user.id)
    )
    await message.answer_photo(photo=shop.photo)
    await message.answer(
        f"Название: {shop.name}\nСоциальные сети: {shop.social_networks}\n "
    )


@router.message(F.text == "Мои товары")
async def show_products(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    page = 0

    products, total_pages = await get_user_products(user_id, page)
    if not products:
        await message.answer("У вас нет товаров 😔")
        return

    markup = generate_pagination_buttons(page, total_pages, user_id)

    await state.clear()
    await state.set_state(MyProducts.pagination)

    current_messages = []

    await message.answer("Ваши товары:", reply_markup=ReplyKeyboardRemove())
    for i in range(len(products)):
        media = [InputMediaPhoto(media=photo) for photo in products[i].photos]
        sent_photos = await message.answer_media_group(media)
        if i == 0 and len(products) > 1:
            sent_text = await message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=ReplyKeyboardRemove(),
            )
        if i == len(products) - 1 and len(products) > 1:
            sent_text = await message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=cancel_button,
            )
        elif i != 0:
            sent_text = await message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
            )
        if len(products) == 1:
            sent_text = await message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=cancel_button,
            )
        current_messages.extend([msg.message_id for msg in sent_photos])
        current_messages.append(sent_text.message_id)
    page_message = await message.answer(
        f"Страница {page + 1} / {total_pages}", reply_markup=markup
    )
    current_messages.append(page_message.message_id)

    await state.update_data(
        chat_id=message.chat.id, current_page=page, current_messages=current_messages
    )


@router.callback_query(lambda c: c.data.startswith(("prev_page", "next_page")))
async def paginate_products(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, user_id, page = callback.data.split(":")
    page = int(page)

    data = await state.get_data()

    for msg_id in data.get("current_messages", []):
        try:
            await bot.delete_message(chat_id=data["chat_id"], message_id=msg_id)
        except Exception as e:
            print(f"❌ Ошибка при удалении {msg_id}: {e}")

    products, total_pages = await get_user_products(user_id, page)
    if not products:
        await callback.message.answer("Товары не найдены!")
        return

    markup = generate_pagination_buttons(page, total_pages, user_id)

    current_messages = []

    for i in range(len(products)):
        media = [InputMediaPhoto(media=photo) for photo in products[i].photos]
        sent_photos = await callback.message.answer_media_group(media)
        if i == 0 and len(products) > 1:
            sent_text = await callback.message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=ReplyKeyboardRemove(),
            )
        if i == len(products) - 1 and len(products) > 1:
            sent_text = await callback.message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=cancel_button,
            )
        elif i != 0:
            sent_text = await callback.message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
            )
        if len(products) == 1:
            sent_text = await callback.message.answer(
                f"Название: {products[i].title}\n"
                f"Описание: {products[i].description}\n"
                f"Цена: {products[i].price} {products[i].currency}",
                reply_markup=cancel_button,
            )
        current_messages.extend([msg.message_id for msg in sent_photos])
        current_messages.append(sent_text.message_id)

    page_message = await callback.message.answer(
        f"Страница {page + 1} / {total_pages}", reply_markup=markup
    )
    current_messages.append(page_message.message_id)

    await state.update_data(current_page=page, current_messages=current_messages)


@router.message(F.text == "Назад")
async def cancel_create_product(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выбрете действие", reply_markup=seller_kb)


@router.message(F.text == "Создать товар")
async def create_product(message: Message, state: FSMContext):
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    await state.set_state(CreateProduct.seller_id)
    await state.update_data(seller_id=str(user.id))
    await state.set_state(CreateProduct.title)
    await message.answer("Введите название товара", reply_markup=cancel_button)


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
    else:
        if not message.photo:
            await message.answer("Пожалуйста, отправьте фото.")
            return
        photos = [message.photo[-1].file_id]

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
    product = await Product.objects.create(
        title=data["title"],
        description=data["description"],
        price=data["price"],
        currency=data["currency"],
        seller_id=data["seller_id"],
        status="active",
        photos=list(data["photos"]),
        category=data["category"],
    )
    product_dict = product.model_dump()
    product_dict["id"] = str(product_dict["id"])
    product_dict["seller_id"] = str(product.seller_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(f"Вы выбрали {callback.data}")
    await es.index(index="products", id=product_dict["id"], body=product_dict)
    await callback.message.answer("Товар создан", reply_markup=seller_kb)

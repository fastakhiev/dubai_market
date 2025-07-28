
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from uuid import UUID

from app.keyboards.buyer import search_filters, search_buttons, categories_list_b, reply_back_buyer, buyer as kb_buyer, \
    orders_list_buttons, back_from_shop_buyer_buttons, my_product_buttons, product_buttons
from app.states.states import SearchFilter, CreateOrder, CreateQuestion
from app.keyboards.common import notification_button
from app.models.orders import Order
from app.models.users import User
from app.models.shops import Shop
from app.models.products import Product
from app.models.questions import Question
from app.core.bot import bot


router = Router()

@router.callback_query(F.data == "search_buyer")
async def go_to_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выбирете фильтр", reply_markup=search_filters)


@router.callback_query(F.data == "without_filter")
async def search_without_filter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SearchFilter.filter)
    await state.set_state(SearchFilter.message)
    message = await callback.message.edit_text("Поиск без фильтра", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "type": "buyer",
        "message_id": message.message_id
    })


@router.callback_query(F.data == "back_from_search")
async def back_from_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Выбирете фильтр", reply_markup=search_filters)
    await callback.answer()


@router.callback_query(lambda c: c.data in categories_list_b)
async def search_with_filter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text(f"Поиск по {callback.data[:-2]}", reply_markup=search_buttons)
    await state.update_data(filter={"category": callback.data[:-2]}, message={
        "type": "buyer",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "back_from_product")
async def back_from_product_buyer(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for i in state_data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=state_data["current_product"]["chat_id"], message_id=i)

    message = await callback.message.answer(f"Поиск по {state_data['filter']['category'] if state_data['filter'] else 'всему'}", reply_markup=search_buttons)
    await state.update_data(filter=state_data["filter"], message={
        "type": "buyer",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "buy_product")
async def buy_product_one(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for i in state_data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=state_data["current_product"]["chat_id"], message_id=i)

    await callback.message.answer("Введите адрес доставки", reply_markup=reply_back_buyer)
    await state.set_state(CreateOrder.address)
    await callback.answer()


@router.message(F.text == "Отменить")
async def back_from_buy_product(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы отменили действие", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберете действие", reply_markup=kb_buyer)


@router.message(CreateOrder.address)
async def create_order_enter_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(CreateOrder.comment)
    await message.answer("Напишите комментарий продавцу")


@router.message(CreateOrder.comment)
async def create_order_enter_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    state_data = await state.get_data()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    await Order.objects.create(
        product_id=UUID(state_data["current_product"]["product_id"]),
        buyer_id=user.id,
        destination=state_data["address"],
        seller_comment=None,
        buyer_comment=state_data["comment"],
        is_approve=False
    )
    product = await Product.objects.select_related("seller_id").get(id=UUID(state_data["current_product"]["product_id"]))
    await bot.send_message(chat_id=product.seller_id.telegram_id, text=f"У вас заказали {product.title}", reply_markup=notification_button)
    await message.answer("Заказ успешно создан\nОжидайте подтверждение продавца, вам придет уведомление", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer("Выберете действие", reply_markup=kb_buyer)


@router.callback_query(F.data == "back_buyer")
async def back_from_filter_buyer(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Выбирете действие", reply_markup=kb_buyer)
    await callback.answer()


@router.callback_query(F.data == "orders_buyer")
async def get_orders_buyer(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.filter)
    await state.set_state(SearchFilter.message)
    message = await callback.message.edit_text("Нажмите для вывода", reply_markup=orders_list_buttons)
    await state.update_data(filter={"orders": str(callback.from_user.id)}, message={
        "type": "buyer",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "questions_buyer")
async def get_questions_buyer(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.filter)
    await state.set_state(SearchFilter.message)
    message = await callback.message.edit_text("Нажмите для вывода", reply_markup=orders_list_buttons)
    await state.update_data(filter={"questions": str(callback.from_user.id)}, message={
        "type": "buyer",
        "message_id": message.message_id
    })
    await callback.answer()


@router.callback_query(F.data == "back_from_order_buyer")
async def back_from_order_buyer(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Выбирете действие", reply_markup=kb_buyer)
    await callback.answer()


@router.callback_query(F.data == "ask_product")
async def ask_about_product(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for i in state_data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=state_data["current_product"]["chat_id"], message_id=i)

    await callback.message.answer("Введите ваш вопрос", reply_markup=reply_back_buyer)
    await state.set_state(CreateQuestion.question)
    await callback.answer()

@router.message(CreateQuestion.question)
async def enter_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    state_data = await state.get_data()
    me = await User.objects.get(telegram_id=str(message.from_user.id))
    product = await Product.objects.select_related("seller_id").get(id=UUID(state_data["current_product"]["product_id"]))
    await Question.objects.create(
        buyer_id=me.id,
        product_id=product.id,
        question=state_data["question"],
        answer=None
    )
    await bot.send_message(chat_id=product.seller_id.telegram_id, text="Вам задали вопрос", reply_markup=notification_button)
    await message.answer("Вопрос отправлен", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer("Выберете действие", reply_markup=kb_buyer)


@router.callback_query(F.data == "get_seller_from_product")
async def get_seller_from_product(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for i in state_data["current_product"]["messages_ids"]:
        await bot.delete_message(chat_id=state_data["current_product"]["chat_id"], message_id=i)
    product = await Product.objects.get(id=UUID(state_data["current_product"]["product_id"]))
    shop = await Shop.objects.select_related("user_id").get(user_id__id=product.seller_id)
    await callback.message.answer_photo(
        photo=f"https://dubaimarketbot.ru/get_image/{shop.photo}",
        caption=f"Название: {shop.name}\n"
        f"Описание: {shop.description}\n"
        f"Социальные сети: {shop.social_networks}\n"
        f"{'Верифицированный продавец' if shop.is_verified else 'Не верифицированный продавец'}",
        reply_markup=back_from_shop_buyer_buttons
    )
    await callback.answer()

@router.callback_query(F.data == "back_from_shop_buyer")
async def back_from_shop_buyer(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await callback.message.delete()
    product = await Product.objects.get(id=UUID(state_data["current_product"]["product_id"]))
    send_photos = await callback.message.answer_media_group(media=[InputMediaPhoto(media=photo) for photo in product.photos])
    send_text = await callback.message.answer(
        f"Название: {product.title}\n"
        f"Описание: {product.description}\n"
        f"Цена: {product.price} {product.currency}\n",
        reply_markup=product_buttons
    )
    messages_ids = []

    messages_ids.extend([msg.message_id for msg in send_photos])
    messages_ids.append(send_text.message_id)
    await state.update_data(current_product={
        "messages_ids": messages_ids,
        "chat_id": callback.message.chat.id,
        "product_id": str(product.id)
    })
    await callback.answer()

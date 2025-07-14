from aiogram import F, Router
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from aiogram.fsm.context import FSMContext
from uuid import UUID

from app.models.products import Product
from app.models.orders import Order
from app.models.questions import Question
from app.states.states import CurrentProduct, CurrentOrder, CurrentQuestion
from app.keyboards.buyer import product_buttons, inline_back_buyer_from_order, my_product_buttons
from app.keyboards.seller import product_inline_buttons_seller, inline_back_button, order_buttons, question_button
from app.core.bot import bot
from app.models.users import User

router = Router()


@router.message(F.text.startswith("question_"))
async def get_question_by_id(message: Message, state: FSMContext):
    try:
        await state.set_state(CurrentQuestion.current_question)
        messages_ids = []
        data = await state.get_data()
        question, user_type = message.text.split(":")
        question_id = question.split("question_")[1]
        question = await Question.objects.select_related("product_id").get(id=UUID(question_id))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
        if user_type == "seller":
            if question.answer:
                keyboard = inline_back_button
            else:
                keyboard = question_button
        else:
            keyboard = inline_back_buyer_from_order
        send_text = await message.answer_photo(
            photo=f"https://dubaimarketbot.ru/get_image/{question.product_id.thumbnail}",
            caption=f"Название: {question.product_id.title}\n"
            f"Описание: {question.product_id.description}\n"
            f"Цена: {question.product_id.price} {question.product_id.currency}\n"
            f"Вопрос: {question.question}\n"
            f"Ответ: {question.answer if question.answer else 'Нет ответа'}\n",
            reply_markup=keyboard
        )
        messages_ids.append(send_text.message_id)
        await state.update_data(current_question={
            "messages_ids": messages_ids,
            "chat_id": message.chat.id,
            "question_id": question_id
        })
    except Exception as e:
        print(e)



@router.message(F.text.startswith("order_"))
async def get_order_by_id(message: Message, state: FSMContext):
    try:
        await state.set_state(CurrentOrder.current_order)
        messages_ids = []
        data = await state.get_data()
        order, user_type = message.text.split(":")
        order_id = order.split("order_")[1]
        order = await Order.objects.select_related("product_id").get(id=UUID(order_id))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
        if user_type == "seller":
            if order.is_approve:
                keyboard = inline_back_button
            else:
                keyboard = order_buttons
        else:
            keyboard = inline_back_buyer_from_order
        send_text = await message.answer_photo(
            photo=f"https://dubaimarketbot.ru/get_image/{order.product_id.thumbnail}",
            caption=f"Название: {order.product_id.title}\n"
            f"Описание: {order.product_id.description}\n"
            f"Цена: {order.product_id.price} {order.product_id.currency}\n"
            f"Адрес: {order.destination}\n"
            f"Комментарий: {order.buyer_comment}\n"
            f"Ответ продавца: {order.seller_comment if order.seller_comment else '-'}\n"
            f"Статус: {'Подтвержден' if order.is_approve else 'Ожидает подтверждения'}",
            reply_markup=keyboard
        )
        messages_ids.append(send_text.message_id)
        await state.update_data(current_order={
            "messages_ids": messages_ids,
            "chat_id": message.chat.id,
            "order_id": order_id
        })
    except Exception as e:
        print(e)

@router.message(F.text.startswith("product_"))
async def get_product_by_id(message: Message, state: FSMContext):
    try:
        await state.set_state(CurrentProduct.current_product)
        messages_ids = []
        data = await state.get_data()
        product, user_type = message.text.split(":")
        product_id = product.split("product_")[1]
        product = await Product.objects.get(id=UUID(product_id))
        user = await User.objects.get(telegram_id=str(message.from_user.id))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
        send_photos = await message.answer_media_group(media=[InputMediaPhoto(media=photo) for photo in product.photos])
        if user_type == "buyer":
            keyboard = my_product_buttons if user.id == product.seller_id.id else product_buttons
        else:
            keyboard = product_inline_buttons_seller
        send_text = await message.answer(
            f"Название: {product.title}\n"
            f"Описание: {product.description}\n"
            f"Цена: {product.price} {product.currency}\n"
            f"{'Это ваш товар' if user.id == product.seller_id.id else ''}",
            reply_markup=keyboard
        )
        messages_ids.extend([msg.message_id for msg in send_photos])
        messages_ids.append(send_text.message_id)
        await state.update_data(current_product = {
            "messages_ids": messages_ids,
            "chat_id": message.chat.id,
            "product_id": product_id
        })

    except Exception as e:
        print(e)
        await message.answer("Что-то пошло не так при обработке product ID")


@router.callback_query(F.data == "delete_notification")
async def delete_notification(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

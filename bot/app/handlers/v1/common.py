from aiogram import F, Router
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from aiogram.fsm.context import FSMContext
from uuid import UUID

from app.models.products import Product
from app.states.states import CurrentProduct
from app.keyboards.buyer import product_buttons
from app.keyboards.seller import product_inline_buttons_seller
from app.core.bot import bot

router = Router()


@router.message(F.text.startswith("product_"))
async def get_product_by_id(message: Message, state: FSMContext):
    try:
        await state.set_state(CurrentProduct.current_product)
        messages_ids = []
        data = await state.get_data()
        product, user_type = message.text.split(":")
        product_id = product.split("product_")[1]
        product = await Product.objects.get(id=UUID(product_id))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
        send_photos = await message.answer_media_group(media=[InputMediaPhoto(media=photo) for photo in product.photos])
        if user_type == "buyer":
            keyboard = product_buttons
        else:
            keyboard = product_inline_buttons_seller
        send_text = await message.answer(
            f"Название: {product.title}\n"
            f"Описание: {product.description}\n"
            f"Цена: {product.price} {product.currency}",
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

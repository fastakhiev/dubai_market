from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.states import CurrentShop
from app.models.shops import Shop
from uuid import UUID
from app.core.bot import bot
from app.keyboards.basic import shop_buttons

router = Router()

@router.message(F.text.startswith("shop_"))
async def get_shop_by_id(message: Message, state: FSMContext):
    try:
        await state.set_state(CurrentShop.current_shop)
        messages_ids = []
        data = await state.get_data()
        shop_id = message.text.split("shop_")[1]
        shop = await Shop.objects.get(id=UUID(shop_id))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
        send_photos = await message.answer_photo(
            photo=f"https://dubaimarketbot.ru/get_image/{shop.photo}",
            caption=f"Название: {shop.name}\nСоциальные сети: {shop.social_networks}\n ",
            reply_markup=shop_buttons
        )
        messages_ids.append(send_photos.message_id)
        await state.update_data(current_shop={
            "messages_ids": messages_ids,
            "chat_id": message.chat.id,
            "shop_id": shop_id
        })
    except Exception as e:
        print(e)
        await message.answer("Что-то пошло не так при обработке shop ID")
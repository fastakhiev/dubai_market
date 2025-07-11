from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from app.states.states import CurrentShop, CurrentProduct
from app.models.shops import Shop
from uuid import UUID
from app.core.bot import bot
from app.keyboards.basic import shop_buttons, product_buttons
from app.models.products import Product

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


@router.message(F.text.startswith("product_"))
async def get_product_by_id(message: Message, state: FSMContext):
    await state.set_state(CurrentProduct.current_product)
    messages_ids = []
    data = await state.get_data()
    product_id = message.text.split("product_")[1]
    product = await Product.objects.get(id=UUID(product_id))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data["message"]["message_id"])
    # send_photos = await message.answer_media_group(media=[InputMediaPhoto(media=photo) for photo in product.photos])
    send_text = await message.answer(
        f"Название: {product.title}\n"
        f"Описание: {product.description}\n"
        f"Цена: {product.price} {product.currency}",
        reply_markup=product_buttons
    )
    # messages_ids.extend([msg.message_id for msg in send_photos])
    messages_ids.append(send_text.message_id)

    await state.update_data(current_product={
        "messages_ids": messages_ids,
        "chat_id": message.chat.id,
        "product_id": product_id
    })

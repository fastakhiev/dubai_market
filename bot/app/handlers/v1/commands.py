from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.models.users import User
from app.states.states import RegSeller, CreateShop
from aiogram.fsm.context import FSMContext
from app.keyboards.seller import seller as kb_seller
from app.keyboards.seller import reg_seller_buttons
from app.keyboards.buyer import buyer as kb_buyer
from app.core.admin_bot import admin_bot
from app.clients.internal_api.file_bucket import FileBucketApi
from app.models.shops import Shop
import ormar
from app.core import config
from app.core.elastic import es

router = Router()


@router.message(F.text == "/seller")
async def change_role_to_seller(message: Message, state: FSMContext):
    await state.clear()
    user = await User.objects.get(telegram_id=str(message.from_user.id))

    try:
        shop = await Shop.objects.get(user_id=user.id)
        await message.answer("Вы переключились на продавца", reply_markup=kb_seller)
    except ormar.exceptions.NoMatch:
        await message.answer(
            "Для того чтобы стать продавцом вам необходимо зарегистрировать аккаунт продавца",
            reply_markup=reg_seller_buttons)


@router.message(CreateShop.name)
async def enter_shop_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateShop.social_networks)
    await message.answer("Введите ваши социальные сети")


@router.message(CreateShop.social_networks)
async def enter_social_networks(message: Message, state: FSMContext):
    await state.update_data(social_networks=message.text)
    await state.set_state(CreateShop.description)
    await message.answer("Добавьте описание своего профиля")


@router.message(CreateShop.description)
async def enter_description_shop(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateShop.photo)
    await message.answer("Загрузите фото вашего профиля")


@router.message(CreateShop.photo)
async def upload_shop_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await FileBucketApi.upload_image(message.photo[-1].file_id)
    data = await state.get_data()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    data["is_verified"] = True if user.passport else False
    data["is_moderation"] = False
    data["user_id"] = user.id
    data["is_active"] = True
    shop = await Shop.objects.create(**data)
    shop_dict = shop.model_dump()
    shop_dict["id"] = str(shop_dict["id"])
    shop_dict["user_id"] = str(shop_dict["user_id"])
    try:
        res = await es.index(index="shops", id=shop_dict["id"], body={
            "id": str(shop.id),
            "name": shop.name,
            "photo": shop.photo,
            "description": shop.description,
            "social_networks": shop.social_networks,
            "user_id": shop_dict["user_id"],
            "is_verified": data["is_verified"],
            "is_active": True,
        })
        print(res)
        print("Indexed successfully")
    except Exception as e:
        import traceback
        print("Ошибка при индексации:")
        traceback.print_exc()
    await state.clear()
    await message.answer("Отлично профиль продавца зарегистрирован", reply_markup=kb_seller)



@router.callback_query(F.data == "reg_seller")
async def reg_seller(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer("Перейдем к созданию профиля продавца, введите название профиля")
    await state.set_state(CreateShop.name)


@router.message(RegSeller.passport)
async def upload_seller_passport(message: Message, state: FSMContext):
    await FileBucketApi.upload_image(message.photo[-1].file_id)
    await state.clear()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    user.passport = message.photo[-1].file_id
    await user.update()
    shop = await Shop.objects.get(user_id=user.id)
    shop.is_moderation = True
    await shop.update()
    await es.update(
        index="shops",
        id=str(shop.id),
        body={
            "doc": {
                "is_moderation": True
            }
        }
    )
    for i in config.ADMIN_TELEGRAM_IDS:
        await admin_bot.send_message(chat_id=i, text=f"{shop.name} загрузил паспорт")
    await message.answer("Отлично, паспорт загружен и отправлен на проверку", reply_markup=kb_seller)



@router.callback_query(F.data == "back_to_buyer")
async def back_to_buyer(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(
        "Вы переключились на покупателя",
        reply_markup=kb_buyer
    )


@router.message(F.text == "/buyer")
async def change_role_to_seller(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы переключились на продавца", reply_markup=kb_buyer)

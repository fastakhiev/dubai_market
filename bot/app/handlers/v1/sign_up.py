from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.signup import main as kb_signup
from app.keyboards.seller import seller as kb_seller
from app.keyboards.buyer import buyer as kb_buyer
from app.core.elastic import es
from app.clients.internal_api.file_bucket import FileBucketApi
from app.states.states import SignUp, CreateShop
from app.models.users import User
from app.models.shops import Shop
import ormar


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    try:
        user = await User.objects.get(telegram_id=str(message.from_user.id))
        if user.role == "seller":
            await message.answer(
                f"С возвращением {user.full_name}", reply_markup=kb_seller
            )
        else:
            await message.answer(
                f"С возвращением {user.full_name}", reply_markup=kb_buyer
            )
    except ormar.exceptions.NoMatch:
        await state.set_state(SignUp.telegram_id)
        await state.update_data(telegram_id=message.from_user.id)
        await message.answer(
            f"Привет выбери тип своего аккаунта", reply_markup=kb_signup
        )


@router.callback_query(F.data == "seller")
async def seller(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SignUp.role)
    await state.update_data(role="seller")
    await state.set_state(SignUp.full_name)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text("Вы продавец")
    await callback.message.answer("Введите ваше полное имя")


@router.callback_query(F.data == "buyer")
async def buyer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SignUp.role)
    await state.update_data(role="buyer")
    await state.set_state(SignUp.full_name)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text("Вы покупатель")
    await callback.message.answer("Введите ваше полное имя")


@router.message(SignUp.full_name)
async def reg_enter_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(SignUp.phone)
    await message.answer("Введите ваш номер телефона")


@router.message(SignUp.phone)
async def reg_enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    if data["role"] == "seller":
        await state.set_state(SignUp.passport)
        await message.answer("Загрузите фото вашего паспорта")
    else:
        data["telegram_id"] = str(data["telegram_id"])
        data["is_active"] = True
        await User.objects.create(**data)
        await message.answer("Вы успешно зарегистрированы")


@router.message(SignUp.passport)
async def reg_upload_passport(message: Message, state: FSMContext):
    await state.update_data(passport=message.photo[-1].file_id)
    await FileBucketApi.upload_image(message.photo[-1].file_id)
    data = await state.get_data()
    data["telegram_id"] = str(data["telegram_id"])
    data["is_active"] = True
    print(data)
    await User.objects.create(**data)
    await state.clear()
    if data["role"] == "seller":
        await state.set_state(CreateShop.name)
        await message.answer("Отлично, перейдем к созданию магазина")
        await message.answer("Введите название вашего магазина")
    else:
        await message.answer("Вы успешно зарегистрированы")


@router.message(CreateShop.name)
async def enter_shop_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateShop.social_networks)
    await message.answer("Введите социальные сети вашего магазина")


@router.message(CreateShop.social_networks)
async def enter_shop_social_networks(message: Message, state: FSMContext):
    await state.update_data(social_networks=message.text)
    await state.set_state(CreateShop.photo)
    await message.answer("Загрузите фото вашего магазина")


@router.message(CreateShop.photo)
async def upload_shop_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await FileBucketApi.upload_image(message.photo[-1].file_id)
    data = await state.get_data()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
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
            "social_networks": shop.social_networks,
            "user_id": shop_dict["user_id"],
            "is_active": True,
        })
        print(res)
        print("Indexed successfully")
    except Exception as e:
        import traceback
        print("Ошибка при индексации:")
        traceback.print_exc()
    await state.clear()
    await message.answer("Отлично магазин зарегистрирован", reply_markup=kb_seller)

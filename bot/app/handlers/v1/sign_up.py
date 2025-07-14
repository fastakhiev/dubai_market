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
    await state.clear()
    try:
        user = await User.objects.get(telegram_id=str(message.from_user.id))
        await message.answer(
            f"С возвращением {user.full_name}\n"
            f"/seller - продавец\n"
            f"/buyer - покупатель",
        )
    except ormar.exceptions.NoMatch:
        await state.set_state(SignUp.telegram_id)
        await state.update_data(telegram_id=message.from_user.id)
        await message.answer(
            f"Здравствуйте!\nУ вас еще нет аккаунта, нужно пройти регистрацию!", reply_markup=kb_signup
        )


@router.callback_query(F.data == "sign_up_all")
async def sign_up_all(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SignUp.full_name)
    await callback.message.edit_reply_markup(reply_markup=None)
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
    data["telegram_id"] = str(data["telegram_id"])
    data["is_active"] = True
    await User.objects.create(**data)
    await state.clear()
    await message.answer("Вы успешно зарегистрированы\n/seller - переключиться на продавца\n/start - перезапуск бота", reply_markup=kb_buyer)

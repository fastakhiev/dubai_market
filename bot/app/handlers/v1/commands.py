from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.models.users import User
from app.states.states import RegSeller, CreateShop
from aiogram.fsm.context import FSMContext
from app.keyboards.seller import seller as kb_seller
from app.keyboards.seller import reg_seller_buttons
from app.keyboards.buyer import buyer as kb_buyer
from app.clients.internal_api.file_bucket import FileBucketApi
from app.models.shops import Shop
import ormar
from app.core.elastic import es

router = Router()


@router.message(F.text == "/seller")
async def change_role_to_seller(message: Message, state: FSMContext):
    await state.clear()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    if user.passport is None:
        await message.answer(
            "Для того чтобы стать продавцом вам необходимо загрузить свой паспорт и зарегистрировать магазин",
            reply_markup=reg_seller_buttons
        )
    else:
        try:
            await Shop.objects.get(user_id=user.id)
            await message.answer("Вы переключились на продавца", reply_markup=kb_seller)
        except ormar.exceptions.NoMatch:
            await message.answer("Вам также необходимо создать магазин\nВведите название вашего магазина")
            await state.set_state(CreateShop.name)


@router.message(CreateShop.name)
async def enter_shop_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateShop.social_networks)
    await message.answer("Введите социальные сети вашего магазина")


@router.message(CreateShop.social_networks)
async def enter_social_networks(message: Message, state: FSMContext):
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



@router.callback_query(F.data == "reg_seller")
async def reg_seller(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegSeller.passport)
    await callback.answer()
    await callback.message.answer("Загрузите фото своего паспорта")


@router.message(RegSeller.passport)
async def upload_seller_passport(message: Message, state: FSMContext):
    await FileBucketApi.upload_image(message.photo[-1].file_id)
    await state.clear()
    user = await User.objects.get(telegram_id=str(message.from_user.id))
    user.passport = message.photo[-1].file_id
    await user.update()
    await message.answer("Отлично, паспорт загружен перейдем к созданию магазина\nВведите название магазина")
    await state.set_state(CreateShop.name)


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

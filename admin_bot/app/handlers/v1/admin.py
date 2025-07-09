from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.basic import basic, search_buttons, seller_buttons, categories_list_b, search_filters
from app.states.states import SearchFilter
from app.models.shops import Shop
from uuid import UUID

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Действия", reply_markup=basic)


@router.callback_query(F.data == "shops")
async def selected_shops(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Поиск по магазинам", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="shops")
    await callback.answer()


@router.callback_query(F.data == "products")
async def go_to_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Выбирете фильтр", reply_markup=search_filters)


@router.callback_query(F.data == "without_filter")
async def search_without_filter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text("Поиск без фильтра", reply_markup=search_buttons)
    await state.update_data(filter={}, message={
        "message_id": message.message_id
    }, type="products")


@router.callback_query(lambda c: c.data in categories_list_b)
async def search_with_filter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchFilter.message)
    await state.set_state(SearchFilter.type)
    await state.set_state(SearchFilter.filter)
    message = await callback.message.edit_text(f"Поиск по {callback.data[:-2]}", reply_markup=search_buttons)
    await state.update_data(filter={"category": callback.data[:-2]}, message={
        "message_id": message.message_id
    }, type="products")
    await callback.answer()



@router.callback_query(F.data == "back_from_search")
async def back_from_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "back_from_search_products")
async def back_from_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "back_from_shop")
async def back_from_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Действия", reply_markup=basic)
    await callback.answer()


@router.callback_query(F.data == "shop_owner_from_shop")
async def get_shop_owner(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    current_shop = await state.get_data()
    shop = await Shop.objects.select_related("user_id").get(id=UUID(current_shop["current_shop"]["shop_id"]))
    await callback.message.answer(f"Имя: {shop.user_id.full_name}\nТелефон: {shop.user_id.phone}\nДата регистрации: {shop.user_id.created_at}\nPassport: {shop.user_id.passport}", reply_markup=seller_buttons)
    await callback.answer()


@router.callback_query(F.data == "back_from_seller")
async def back_from_shop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Действия", reply_markup=basic)
    await callback.answer()

from aiogram.fsm.state import StatesGroup, State


class SignUp(StatesGroup):
    telegram_id = State()
    full_name = State()
    phone = State()
    passport = State()
    role = State()


class SearchFilter(StatesGroup):
    filter = State()
    message = State()


class CreateShop(StatesGroup):
    name = State()
    photo = State()
    social_networks = State()


class CreateProduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    currency = State()
    seller_id = State()
    status = State()
    photos = State()
    category = State()


class MyProducts(StatesGroup):
    pagination = State()


class CurrentProduct(StatesGroup):
    current_product = State()


class CreateOrder(StatesGroup):
    address = State()
    comment = State()
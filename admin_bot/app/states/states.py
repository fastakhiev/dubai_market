from aiogram.fsm.state import StatesGroup, State


class SearchFilter(StatesGroup):
    filter = State()
    type = State()
    message = State()


class CurrentShop(StatesGroup):
    current_shop = State()


class CurrentProduct(StatesGroup):
    current_product = State()


class CurrentOwner(StatesGroup):
    current_owner = State()

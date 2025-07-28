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


class RejectProduct(StatesGroup):
    problem_product = State()
    telegram_id = State()


class RejectPassport(StatesGroup):
    problem_passport = State()
    telegram_id = State()


class ApproveProduct(StatesGroup):
    problem_approve_product = State()
    telegram_id = State()

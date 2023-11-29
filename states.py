from aiogram.fsm.state import State, StatesGroup


class UserAndAdminState(StatesGroup):
    admin = State()
    user = State()


class AdminStates(StatesGroup):
    menu_state = State()
    spam = State()
    black_list = State()
    white_list = State()
    statistics = State()

class UserStates(StatesGroup):
    menu_state = State()



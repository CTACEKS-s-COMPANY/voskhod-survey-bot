from aiogram.fsm.state import State, StatesGroup


class UserAndAdminState(StatesGroup):
    admin = State()
    user = State()


class adminStates(StatesGroup):
    spam = State()
    black_list = State()
    white_list = State()

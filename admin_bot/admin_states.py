from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    menu_state = State()
    spam = State()
    black_list = State()
    white_list = State()
    statistics = State()
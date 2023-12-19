from aiogram.fsm.state import State, StatesGroup


class PostStates(StatesGroup):
    title_state = State()
    text_state = State()
    date_state = State()
    that_right_state = State()


class BaseAdminStates(StatesGroup):
    new_admin = State()
    in_admin_state = State()
    you_not_admin = State()


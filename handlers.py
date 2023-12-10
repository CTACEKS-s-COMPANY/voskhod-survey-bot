import kb
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from res import states, text

router = Router()

ADMIN_ID = 541852628  # Узнать можно тут @getmyid_bot


# Bot /Start message
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        await msg.answer(text.greet_admin.format(name=msg.from_user.full_name), reply_markup=kb.menu_admin)
        await state.set_state(states.AdminStates.menu_state)
    else:
        await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=kb.menu_user)
        await state.set_state(states.UserStates.menu_state)


# User functions 👶🏻
# Menu open commands
@router.message(states.UserStates.menu_state)
async def hello_user_command(msg=Message):
    await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=kb.menu_user)


# Answer about user's health
@router.callback_query(states.UserStates.menu_state, F.data == "die")
async def health_reply(clbck: Message, state: FSMContext):
    await clbck.message.answer(text.die_answer)


# Answer about user's vacation

@router.callback_query(states.UserStates.menu_state, F.data == "travel")
async def vacation_reply(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.vacation_answer)


# Admin functions ‍💼
# Admin menu
@router.message(states.AdminStates.menu_state)  # works with [AdminStates.menu]
async def hello_admin_command(msg=Message):
    await msg.answer(text.greet_admin.format(name=msg.from_user.full_name), reply_markup=kb.menu_admin)


# Going to spam from menu by keyboard button
@router.callback_query(states.AdminStates.menu_state, F.data == "spam")
async def spam_command(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer('Напишите текст рассылки')
    await state.set_state(states.AdminStates.spam)


@router.message(states.AdminStates.spam)
async def start_spam(msg: Message):
    await msg.answer(text="Hello")
    print("I'm in spam")


# Going to statistics menu by keyboard button
@router.callback_query(states.AdminStates.menu_state, F.data == "statistics")
async def statistics_command(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Вот ваша статистика")
    await state.set_state(states.AdminStates.statistics)


# Going to black_list menu by keyboard action
@router.callback_query(states.AdminStates.menu_state, F.data == "add_black_list")
async def black_list_command(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Вы в меню черного списка")
    await state.set_state(states.AdminStates.black_list)


@router.callback_query(states.AdminStates.black_list)
async def start_black_list(msg: Message, state: FSMContext):
    await msg.answer(text="You in black list")
    print("I'm in black list")
    # await state.set_state(states.AdminStates.menu_state)

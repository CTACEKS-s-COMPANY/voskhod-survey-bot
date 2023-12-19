from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pydantic import ValidationError
import re
from app.admin_bot_package.admin_states import PostStates, BaseAdminStates
from app.admin_bot_package.res import admin_kb, admin_text as text
from app.utils.data import db
from app.utils.data.db import set_user_to_admin, new_post, send_post

admin_router = Router()


# ToDO Сделать всос текста в HTML, чтобы сохранять форматирования текста в Телеге

# Admin functions ‍💼
# Admin menu"# works with [AdminStates.menu]
@admin_router.message(Command("start"))
async def hello_admin_command(msg: Message, state: FSMContext):
    is_admin = db.does_user_admin(msg.from_user.id)
    if is_admin:
        await msg.answer(text.greet_admin.format(name = msg.from_user.full_name), reply_markup=admin_kb.menu_kb)
        await state.set_state(BaseAdminStates.in_admin_state)
    else:
        await msg.answer(text=text.you_are_not_admin_message,
                         reply_markup=admin_kb.you_are_not_admin_kb, parse_mode=ParseMode.HTML)
        await state.set_state(BaseAdminStates.you_not_admin)


@admin_router.message(StateFilter(BaseAdminStates.you_not_admin))
async def you_not_admin(msg: Message, state: FSMContext):
    await msg.answer(text.lets_try_again_message,parse_mode=ParseMode.HTML)
    is_admin = db.does_user_admin(msg.from_user.id)
    if is_admin:
        await msg.answer(text=text.greet_admin.format(name = msg.from_user.full_name), reply_markup=admin_kb.menu_kb)
        await state.set_state(None)
    else:
        await msg.answer(text=text.dont_work)


# New Admin State
@admin_router.message(StateFilter(BaseAdminStates.in_admin_state), F.text == text.insert_admin_button)
async def make_user_admin(msg: Message, state: FSMContext):
    await msg.answer(text.insert_admin_message)
    await state.set_state(BaseAdminStates.new_admin)


@admin_router.message(StateFilter(BaseAdminStates.new_admin))
async def new_admin(msg: Message, state: FSMContext):
    # regex id finder
    user_id_from_message = re.findall("\d+", msg.text.lower())[0]
    # id = msg.text.split(" ")[3]
    await msg.answer(set_user_to_admin(user_id_from_message))
    await state.set_state(BaseAdminStates.in_admin_state)


# Post states
@admin_router.message(StateFilter(BaseAdminStates.in_admin_state), F.text == text.insert_post_button)
async def post_admin_command(msg: Message, state: FSMContext):
    await msg.answer(text=text.insert_post_message)
    await state.set_state(PostStates.text_state)

# ToDo how to make back button reply_markup=admin_kb.back_menu_kb
# Input title
# @admin_router.message(StateFilter(PostStates.title_state))
# async def title_input(msg: Message, state: FSMContext):
#     await msg.answer(text=f"{msg.html_text}\n\nВведите текст поста", parse_mode=ParseMode.HTML)
#     await state.set_state(PostStates.text_state)

# ToDo make title input
# Input text
@admin_router.message(StateFilter(PostStates.text_state))
async def text_input(msg: Message, state: FSMContext):
    await msg.answer(f"{new_post(msg.from_user.id, msg.html_text)}\n", parse_mode=ParseMode.HTML)
    try:
        await msg.answer(await send_post(msg.from_user.id))
    except ValidationError as error:
        print(error)
    await msg.answer("Ваше сообщение отправлено", reply_markup=admin_kb.menu_kb, parse_mode=ParseMode.HTML)
    await state.set_state(BaseAdminStates.in_admin_state)
    # await commit_changes()


#  Input date
@admin_router.message(StateFilter(PostStates.date_state))
async def data_input(msg: Message, state: FSMContext):
    await msg.answer(text=f"Дата: {datetime.now()}", parse_mode=ParseMode.HTML)
    await state.set_state(PostStates.that_right_state)


# @admin_router.message(StateFilter(PostStates.that_right_state))
# async def that_right_input(msg: Message, state: FSMContext):
#     await msg.answer(text="Ваше сообщение:\n", reply_markup=admin_kb.that_right_state_kb)
#
#
# @admin_router.callback_query(StateFilter(PostStates.that_right_state), F.data == "yes_button")
# async def yes_button(callback: CallbackQuery, state: FSMContext):
#     await callback.answer(text="Нажата кнопка Да")
#     await state.set_state(None)
#
#
# @admin_router.callback_query(StateFilter(PostStates.that_right_state), F.data == "no_button")
# async def no_button(msg: Message, state: FSMContext):
#     await msg.answer(text="No,button pressed")
#     await state.set_state(PostStates.title_state)


# Registration in bot and start commands

@admin_router.message(StateFilter(BaseAdminStates.in_admin_state))
async def nothing_in_admin(msg: Message):
    await msg.answer(text="Выберите команду", reply_markup=admin_kb.menu_kb)

@admin_router.message()
async def nothing_before(msg: Message, state: FSMContext):
    await msg.answer("Введите команду /start")
# New admin state

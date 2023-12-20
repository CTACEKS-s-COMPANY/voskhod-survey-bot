import asyncio
import re
from datetime import datetime

import psycopg2
from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from app import config
from app.admin_bot_package.admin_states import PostStates, BaseAdminStates
from app.admin_bot_package.res import admin_kb, admin_text as text
from app.utils.data.database import db

admin_router = Router()


# ToDO Сделать всос текста в HTML, чтобы сохранять форматирования текста в Телеге

# Admin functions ‍💼
# Admin menu# works with [AdminStates.menu]
@admin_router.message(Command("start"))
async def hello_admin_command(msg: Message, state: FSMContext):
    try:
        is_admin = db.does_user_admin(msg.from_user.id)
        if is_admin:
            await msg.answer(text.greet_admin.format(name=msg.from_user.full_name), reply_markup=admin_kb.menu_kb)
            await state.set_state(BaseAdminStates.in_admin_state)
        else:
            await msg.answer(text=text.you_are_not_admin_message,
                             reply_markup=admin_kb.you_are_not_admin_kb, parse_mode=ParseMode.HTML)
            await state.set_state(BaseAdminStates.you_not_admin)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        await msg.answer(text.something_goes_wrong)
        await state.set_state(BaseAdminStates.in_admin_state)


@admin_router.message(StateFilter(BaseAdminStates.you_not_admin))
async def you_not_admin(msg: Message, state: FSMContext):
    await msg.answer(text.lets_try_again_message, parse_mode=ParseMode.HTML)
    is_admin = db.does_user_admin(msg.from_user.id)
    if is_admin:
        await msg.answer(text=text.greet_admin.format(name=msg.from_user.full_name), reply_markup=admin_kb.menu_kb)
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
    try:
        await db.set_user_to_admin(user_id_from_message)
        await msg.answer(text.new_one_admin_message)
        await state.set_state(BaseAdminStates.in_admin_state)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        await msg.answer(text.something_goes_wrong)
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
    try:
        # getting messages
        logger.info("Getting message")
        await db.new_post(msg.from_user.id,msg.html_text)
        post = await db.get_post(msg.from_user.id)
        subscribers = await db.get_subscribers()
        logger.info(f"Sending post from {msg.from_user.id}")
        logger.info(f"Sending post is: {post}")
        logger.info(f"All subscribers: {subscribers}")
        # sending messages
        operator = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
        for subscriber in subscribers:
            logger.info(subscriber[0])
            await operator.send_message(str(subscriber[0]), post)
            await asyncio.sleep(5)
        await operator.close()
        await msg.answer("Ваше сообщение отправлено",
                         reply_markup=admin_kb.menu_kb,
                         parse_mode=ParseMode.HTML)
        # changing state
        await state.set_state(BaseAdminStates.in_admin_state)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        await msg.answer(text.something_goes_wrong)
        await state.set_state(BaseAdminStates.in_admin_state)


#  Input date
@admin_router.message(StateFilter(PostStates.date_state))
async def data_input(msg: Message, state: FSMContext):
    await msg.answer(text=f"Дата: {datetime.now()}", parse_mode=ParseMode.HTML)
    await state.set_state(PostStates.that_right_state)

# Registration in bot and start commands

@admin_router.message(StateFilter(BaseAdminStates.in_admin_state))
async def nothing_in_admin(msg: Message):
    await msg.answer(text="Выберите команду", reply_markup=admin_kb.menu_kb)


@admin_router.message()
async def nothing_before(msg: Message):
    await msg.answer("Введите команду /start")

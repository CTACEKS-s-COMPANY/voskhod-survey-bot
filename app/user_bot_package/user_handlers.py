import re

import psycopg2
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger

from app.utils.data.database import db

user_router = Router()
from app.user_bot_package.res import user_text as text, user_kb


# User functions 👶🏻
# Menu open commands

# Null message
@user_router.message(Command("start"))
async def start_handler(msg: Message):
    db.create_user(msg.from_user.id)  # Создание клиента в бд
    await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=user_kb.subscribe_kb)


# Bot /Start message
@user_router.message(Command("id"))
async def id_handler(msg: Message):
    await msg.answer(text.id_answer.format(id=msg.from_user.id), parse_mode=ParseMode.HTML)


# Subscribe state
@user_router.message(F.text == text.subscribe_to_newsletter_trigger)
async def subscribe_to_newsletter(msg: Message):
    # Залезть в базу и поставить галочку на рассылку
    if db.does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer(text.subscribe_to_newsletter_answer, reply_markup=None)
    else:
        await msg.answer(str(db.set_subscribe_to_newsletter(msg.from_user.id)))


@user_router.message(StateFilter(None))
async def greet_user(msg: Message):
    # Проверка на рассылку

    if db.does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer(text=text.you_already_subscribe_to_newsletter)
    else:
        await msg.answer(text=text.you_already_not_subscribe_to_newsletter)


@user_router.callback_query(F.data == "yes_button")
async def yes_button_clicked(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer(clbck.message.text)
    post_id_from_message = re.findall("\d+", clbck.message.text)[0]
    try:
        await db.create_answer(clbck.from_user.id, post_id_from_message, True)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


@user_router.callback_query(F.data == "no_button")
async def no_button_clicked(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer(clbck.message.text)
    post_id_from_message = re.findall("\d+", clbck.message.text)[0]
    try:
        await db.create_answer(clbck.from_user.id, post_id_from_message,False)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.utils.data.db import create_user, set_subscribe_to_newsletter, does_user_subscribe_to_newsletter

user_router = Router()
from app.user_bot_package.res import user_text as text, user_kb


# User functions 👶🏻
# Menu open commands

# Null message
@user_router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    create_user(msg.from_user.id)  # Создание клиента в бд
    await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=user_kb.subscribe_kb)


# Bot /Start message
@user_router.message(Command("id"))
async def id_handler(msg: Message, state: FSMContext):
    await msg.answer(text.id_answer.format(id=msg.from_user.id), parse_mode=ParseMode.HTML)


# Subscribe state
@user_router.message(F.text == text.subscribe_to_newsletter_trigger)
async def subscribe_to_newsletter(msg: Message, state: FSMContext):
    # Залезть в базу и поставить галочку на рассылку
    if does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer(text.subscribe_to_newsletter_answer, reply_markup=None)
    else:
        await msg.answer(str(set_subscribe_to_newsletter(msg.from_user.id)))


@user_router.message(StateFilter(None))
async def greet_user(msg: Message, state: FSMContext):
    # Проверка на рассылку

    if does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer(text=text.you_already_subscribe_to_newsletter)
    else:
        await msg.answer(text=text.you_already_not_subscribe_to_newsletter)

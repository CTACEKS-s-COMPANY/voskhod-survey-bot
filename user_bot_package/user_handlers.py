from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.data.db import get_user, create_user, set_subscribe_to_newsletter, does_user_subscribe_to_newsletter

user_router = Router()
from user_bot_package.res import user_text as text
from user_bot_package.res import user_kb


# User functions 👶🏻
# Menu open commands

# Null message
@user_router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    create_user(msg.from_user.id)  # Создание клиента в бд
    await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=user_kb.subscribe_kb)
    # await state.set_state(UserStates.subscribe_state)


# Bot /Start message
@user_router.message(Command("id"))
async def id_handler(msg: Message, state: FSMContext):
    await msg.answer(f"Ваш ID - {str(msg.from_user.id)} \n"
                     f"Перешлите это сообщение пользователю, который собирается дать вам права Админа")
    data = get_user(msg.from_user.id)
    await msg.answer(f"ID: {data[0][0]}\n You are subscribed: {data[0][1]}\n You are admin: {data[0][2]} \n "
                     f"Date: {data[0][3]}\n")


# Subscribe state
@user_router.message(F.text == text.subscribe_to_newsletter)
async def subscribe_to_newsletter(msg: Message, state: FSMContext):
    # Залезть в базу и поставить галочку на рассылку
    if does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer("Вы уже подписались на рассылку", reply_markup=None)
    else:
        await msg.answer(str(set_subscribe_to_newsletter(msg.from_user.id)))


@user_router.message(StateFilter(None))
async def greet_user(msg: Message, state: FSMContext):
    # Проверка на рассылку

    if does_user_subscribe_to_newsletter(msg.from_user.id) is True:
        await msg.answer("Вы уже подписались на рассылку")
    else:
        await msg.answer("Вы еще не подписались на рассылку")

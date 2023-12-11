from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.data.db import get_users, create_user

user_router = Router()
from user_bot.res import user_text as text
from user_bot.res import user_kb
from user_bot.user_states import UserStates


# User functions 👶🏻
# Menu open commands

# Null message
@user_router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    # Создать клиента в бд
    create_user(msg.from_user.id)
    await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=user_kb.subscribe_kb)
    await state.set_state(UserStates.subscribe_state)


# Bot /Start message
@user_router.message(Command("id"))
async def id_handler(msg: Message, state: FSMContext):
    await msg.answer("Your ID is\n" + str(msg.from_user.id))

    data = get_users()

    await msg.answer(f"Data: {data}")


# Subscribe state
@user_router.message(StateFilter(UserStates.subscribe_state), F.text == text.subscribe_to_newsletter)
async def subscribe_to_newsletter(msg: Message, state: FSMContext):
    id = msg.from_user.id
    # Залезть в базу и поставить галочку на рассылку
    await msg.answer(text="Отлично, теперь вы подписались на рассылку", )
    await state.set_state(None)


@user_router.message(UserStates.subscribe_state)
async def hello_user_command(msg=Message):
    await msg.answer(
        text=text.greet_user.format(name=msg.from_user.full_name),
        reply_markup=user_kb.subscribe_kb)


@user_router.message()
async def greet_user(msg: Message, state: FSMContext):
    # Проверка на рассылку
    id = msg.from_user.id
    a = True
    if a:
        await msg.answer("Вы уже подписались на рассылку")
    else:
        await msg.answer("Вы еще не подписались на рассылку")


async def send_message_from_admin(text: str, msg: Message):
    await msg.answer(text=text)

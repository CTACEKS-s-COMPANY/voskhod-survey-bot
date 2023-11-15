import dp
from aiogram import F, Router, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message

# Внутренние классы
import config
import kb
import states
import text

router = Router()

# Bot /Start message
@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.from_user.id == config.ADMIN_ID:
        await msg.answer(text.greet_admin.format(name=msg.from_user.full_name), reply_markup=kb.menu_admin)
    else:
        await msg.answer(text.greet_user.format(name=msg.from_user.full_name), reply_markup=kb.menu_user)


# Menu open commands
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.reply(text.menu, reply_markup=kb.menu_user)


# User functions 👶🏻
# Answer about user's health
@router.callback_query(F.data == "die")
async def health_reply(clbck: Message, state: FSMContext):
    await clbck.message.answer(text.die_answer)


# Answer about user's vacation
@router.callback_query(F.data == "travel")
async def vacation_reply(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.vacation_answer)


# Admin functions 👩🏻‍💼
@router.callback_query(F.data == "spam")
async def spam_command(msg=Message):
    await states.adminStates.spam.set()
    await msg.message.answer('Напишите текст рассылки')


# @dp.message_handler(state=states.adminStates.spam)
# async def start_spam(msg: Message, state: FSMContext):
#     await msg.message.answer(msg.text)

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import kb
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "die")
async def die_reply(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer(text.die_answer)

@router.callback_query(F.data == "travel")
async def die_reply(clbck: CallbackQuery, state: FSMContext):
    await clbck.answer(text.travel_answer)
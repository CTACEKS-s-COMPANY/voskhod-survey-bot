from aiogram import Router
from aiogram.types import Message

admin_router = Router()

ADMIN_ID = 541852628  # Узнать можно тут @getmyid_bot


# Admin functions ‍💼
# Admin menu
@admin_router.message()  # works with [AdminStates.menu]
async def hello_admin_command(msg=Message):
    await msg.answer("Hello admin!")



# ToDO Сделать всос текста в HTML, чтобы сохранять форматирования текста в Телеге

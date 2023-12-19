# https://habr.com/ru/articles/732136/
# https://habr.com/ru/articles/599199/
# https://mastergroosha.github.io/aiogram-3-guide/fsm/
# https://github.com/rdfsx/schedule_bot

import asyncio  # Для ассинхронного запуска бота
import logging  # Для настройки логгирования, которое поможет в отладке

import psycopg2
from aiogram import Dispatcher, Bot, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app import config
from app.admin_bot_package.admin_handlers import admin_router
from app.user_bot_package.user_handlers import user_router
from app.utils.data import database

# funktion with bots polling
async def bot_poll(bot: Bot, router: Router):
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

user_bot = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
admin_bot = Bot(config.ADMIN_BOT_ID, parse_mode=ParseMode.HTML)

async def main():
    load_dotenv()
    database.start_up()

    await asyncio.gather(
        bot_poll(user_bot, user_router),
        bot_poll(admin_bot, admin_router),
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

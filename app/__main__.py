# https://habr.com/ru/articles/732136/
# https://habr.com/ru/articles/599199/
# https://mastergroosha.github.io/aiogram-3-guide/fsm/
# https://github.com/rdfsx/schedule_bot

import asyncio  # Для ассинхронного запуска бота
import logging  # Для настройки логгирования, которое поможет в отладке

from aiogram import Dispatcher, Bot, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app import config
from app.admin_bot_package.admin_handlers import admin_router
from app.user_bot_package.user_handlers import user_router
from app.utils.data import database


async def on_startup() -> None:
    load_dotenv()
    database.start_up()


async def main():
    user_bot = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
    admin_bot = Bot(config.ADMIN_BOT_ID, parse_mode=ParseMode.HTML)

    dp_user = Dispatcher(storage=MemoryStorage())
    dp_user.include_router(user_router)

    dp_admin = Dispatcher(storage=MemoryStorage())
    dp_admin.include_router(admin_router)

    dp_user.startup.register(on_startup)

    await asyncio.gather(
        dp_admin.start_polling(admin_bot, allowed_updates=dp_user.resolve_used_update_types()),
        dp_user.start_polling(user_bot, allowed_updates=dp_user.resolve_used_update_types())
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

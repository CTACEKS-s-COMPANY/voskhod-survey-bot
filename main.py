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

import config
from admin_bot_package.admin_handlers import admin_router
from user_bot_package.user_handlers import user_router

admin_bot = Bot(config.ADMIN_BOT_ID, parse_mode=ParseMode.HTML)
user_bot = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)


# funktion with bots polling
async def bot_poll(bot: Bot, router: Router):
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def main():
    load_dotenv()
    await asyncio.gather(
        bot_poll(user_bot, user_router),
        bot_poll(admin_bot, admin_router)
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

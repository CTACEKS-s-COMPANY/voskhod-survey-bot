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
from user_bot.user_handlers import user_router
from admin_bot.admin_handlers import admin_router

# funktion with bots polling
async def bot_poll(token,router: Router):
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def main():
    load_dotenv()
    await asyncio.create_task(bot_poll(config.USER_BOT_TOKEN, user_router))
    # await asyncio.create_task(bot_poll(config.ADMIN_BOT_ID,admin_router))



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

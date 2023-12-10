# https://habr.com/ru/articles/732136/
# https://habr.com/ru/articles/599199/
# https://mastergroosha.github.io/aiogram-3-guide/fsm/
# https://github.com/rdfsx/schedule_bot

import os
import asyncio  # Для ассинхронного запуска бота
import logging  # Для настройки логгирования, которое поможет в отладке
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import router

BOT_TOKEN = os.getenv("BOT_TOKEN")
async def main():
    load_dotenv()

    print(BOT_TOKEN)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from user_bot.res import user_text as text

# Menu buttons and keyboard buttons of USER
subscribe_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.subscribe_to_newsletter)]], one_time_keyboard=True)


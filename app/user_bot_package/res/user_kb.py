from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.user_bot_package.res import user_text as text

# Menu buttons and keyboard buttons of USER
subscribe_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text.subscribe_to_newsletter_trigger)]],
                                   one_time_keyboard=True, resize_keyboard=True)




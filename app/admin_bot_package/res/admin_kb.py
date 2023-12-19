from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Menu buttons and keyboard buttons of Admin
menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Новый пост"), KeyboardButton(text="Статистика"),
     KeyboardButton(text="Добавить админа")]
], one_time_keyboard=True, resize_keyboard=True)

back_menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Back")]
])

that_right_state_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Да", callback_data="yes_button"),
    InlineKeyboardButton(text="Нет", callback_data="no_button")
]])

you_are_not_admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Попробовать еще раз")]
], resize_keyboard=True)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from res import text

# Menu buttons and keyboard buttons of USER
menu_user_buttons = [
    [InlineKeyboardButton(text=text.health_btn, callback_data="die"),
     InlineKeyboardButton(text=text.vacation_btn, callback_data="travel")]
]
menu_user = InlineKeyboardMarkup(inline_keyboard=menu_user_buttons)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

# Menu buttons and keyboard buttons of ROOT_USER
menu_admin_buttons = [
    [InlineKeyboardButton(text="Рассылка", callback_data="spam"),
     InlineKeyboardButton(text="Добавить в ЧС", callback_data="add_black_list")],
    [InlineKeyboardButton(text="Убрать из ЧС", callback_data="clear_black_list"),
     InlineKeyboardButton(text="Статистика", callback_data="statistics")]
]
menu_admin = InlineKeyboardMarkup(inline_keyboard=menu_admin_buttons)

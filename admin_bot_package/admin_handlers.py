from datetime import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pydantic import ValidationError

from admin_bot_package.admin_states import PostStates, BaseAdminStates
from admin_bot_package.res import admin_kb
from utils.data import db
from utils.data.db import set_user_to_admin, new_post, send_post

admin_router = Router()

ADMIN_ID = 541852628  # Узнать можно тут @getmyid_bot


# ToDO Сделать всос текста в HTML, чтобы сохранять форматирования текста в Телеге

# Admin functions ‍💼
# Admin menu"# works with [AdminStates.menu]
@admin_router.message(Command("start"))
async def hello_admin_command(msg: Message, state: FSMContext):
    is_admin = db.does_user_admin(msg.from_user.id)
    if is_admin:
        await msg.answer(text="Здравствуйте, Админ", reply_markup=admin_kb.menu_kb)
        await state.set_state(BaseAdminStates.in_admin_state)
    else:
        await msg.answer(text="Извините, вы не админ\n"
                              "Попросите другого пользователя с правами Админа нажать кнопку \"Добавить админа\"",
                         reply_markup=admin_kb.you_are_not_admin_kb)
        await state.set_state(BaseAdminStates.you_not_admin)


@admin_router.message(StateFilter(BaseAdminStates.you_not_admin))
async def you_not_admin(msg: Message, state: FSMContext):
    await msg.answer("Хорошо, давайте еще разок попробуем...")
    is_admin = db.does_user_admin(msg.from_user.id)
    if is_admin:
        await msg.answer(text="Здравствуйте, Админ", reply_markup=admin_kb.menu_kb)
        await state.set_state(None)
    else:
        await msg.answer(text="Не сработало")


# New Admin State
@admin_router.message(StateFilter(BaseAdminStates.in_admin_state), F.text == "Добавить админа")
async def make_user_admin(msg: Message, state: FSMContext):
    await msg.answer("Попросите пользователя зарегистрироваться в \n"
                     "@voskhod_survey_bot и ввести комманду /id\n"
                     "Перешлите сообщение сюда")
    await state.set_state(BaseAdminStates.new_admin)


@admin_router.message(StateFilter(BaseAdminStates.new_admin))
async def new_admin(msg: Message, state: FSMContext):
    id = msg.text.split(" ")[3]
    await msg.answer(set_user_to_admin(id))
    await state.set_state(None)


# Post states
@admin_router.message(StateFilter(BaseAdminStates.in_admin_state), F.text == "Новый пост")
async def post_admin_command(msg: Message, state: FSMContext):
    await state.set_state(PostStates.title_state)
    await msg.answer(text="Введите тему вашего Поста")


# ToDo how to make back button reply_markup=admin_kb.back_menu_kb
# Input title
@admin_router.message(StateFilter(PostStates.title_state))
async def title_input(msg: Message, state: FSMContext):
    await msg.answer(text=f"{msg.html_text}\n\nВведите текст поста", parse_mode=ParseMode.HTML)
    await state.set_state(PostStates.text_state)

# ToDo make title input
# Input text
@admin_router.message(StateFilter(PostStates.text_state))
async def text_input(msg: Message, state: FSMContext):
    await msg.answer(f"{new_post(msg.from_user.id, str(msg.html_text))}\n", parse_mode=ParseMode.HTML)
    try:
        await msg.answer(await send_post(msg.from_user.id))
        # operator = Bot(config.USER_BOT_TOKEN,parse_mode=ParseMode.HTML)
        # await operator.send_message(756263716,"Стас, хоть я и бот, но все-равно вижу, что ты дрочишь")
        # await operator.close()
    except ValidationError as error:
        print(error)
    await msg.answer("Ваше сообщение отправлено", reply_markup=admin_kb.menu_kb, parse_mode=ParseMode.HTML)
    await state.set_state(None)
    # await commit_changes()


#  Input date
@admin_router.message(StateFilter(PostStates.date_state))
async def data_input(msg: Message, state: FSMContext):
    await msg.answer(text=f"Дата: {datetime.now()}", parse_mode=ParseMode.HTML)
    await state.set_state(PostStates.that_right_state)


# @admin_router.message(StateFilter(PostStates.that_right_state))
# async def that_right_input(msg: Message, state: FSMContext):
#     await msg.answer(text="Ваше сообщение:\n", reply_markup=admin_kb.that_right_state_kb)
#
#
# @admin_router.callback_query(StateFilter(PostStates.that_right_state), F.data == "yes_button")
# async def yes_button(callback: CallbackQuery, state: FSMContext):
#     await callback.answer(text="Нажата кнопка Да")
#     await state.set_state(None)
#
#
# @admin_router.callback_query(StateFilter(PostStates.that_right_state), F.data == "no_button")
# async def no_button(msg: Message, state: FSMContext):
#     await msg.answer(text="No,button pressed")
#     await state.set_state(PostStates.title_state)


# Registration in bot and start commands

@admin_router.message(StateFilter(BaseAdminStates.in_admin_state))
async def nothing_in_admin(msg: Message):
    await msg.answer(text="Выберите команду",reply_markup=admin_kb.menu_kb)

@admin_router.message()
async def nothing_before(msg: Message, state: FSMContext):
    await msg.answer("Введите команду /start")
# New admin state

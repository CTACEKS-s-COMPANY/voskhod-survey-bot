import aiogram.handlers
import psycopg2
from aiogram import Bot
from aiogram.enums import ParseMode
from pydantic import ValidationError

import config

db_connection = psycopg2.connect(config.POSTGRES_URI, sslmode="disable")
db_object = db_connection.cursor()


# DB for user
# Сохраняем текущее «состояние» пользователя в нашу базу
def create_user(user_id: int):
    try:
        db_object.execute(f"SELECT id FROM users WHERE id  = {user_id}")
        result = db_object.fetchone()
        if result is None:
            db_object.execute(f"INSERT INTO users (id) VALUES ('{user_id}')")
            db_connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


# Получаем текущее состояние пользователя
def get_user(user_id: int):
    try:
        db_object.execute(f"SELECT * from users where id={user_id}")
        result = db_object.fetchall()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return f"Что то пошло не так {error}"


def set_subscribe_to_newsletter(user_id: int):
    try:
        db_object.execute(f'UPDATE users SET is_subscriber = true WHERE id ={user_id};')
        db_connection.commit()
        return "Отлично, теперь вы подписались на рассылку"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return f"Что то пошло не так {error}"


def does_user_subscribe_to_newsletter(user_id: int):
    db_object.execute(f"SELECT * from users where id={user_id}")
    user = db_object.fetchall()
    return user[0][1]


# DB for admin
def does_user_admin(user_id: int):
    create_user(user_id)
    db_object.execute(f"SELECT * from users where id={user_id}")
    user = db_object.fetchall()
    return user[0][2]


def set_user_to_admin(user_id: str):
    try:
        db_object.execute(f'UPDATE users SET is_admin = true WHERE id ={user_id};')
        db_connection.commit()
        return "Отлично, теперь на одного админа больше"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return f"Что то пошло не так {error}"


# Making messages
# ToDo make more 1 row with title
def new_post(user_id: int, text: str):
    try:
        db_object.execute(f"INSERT INTO posts (author_id,text) VALUES ('{user_id}','{text}')")
        db_connection.commit()
        return text
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "Something went wrong"

# TODO - шедуле
async def send_post(user_id: int):
    try:
        if config.ADMIN_BOT_ID is not None:
            operator = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
            await operator.send_message(user_id,"Проверка")
            await operator.close()
        else:
            raise Exception("ADMIN BOT ID not defined")
    except ValidationError as error:
        print(error)


import asyncio
import re

import psycopg2
from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger

from app import config
from app.utils.data import db_text as text

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
        return text.something_goes_wrong(error=error)


def set_subscribe_to_newsletter(user_id: int):
    try:
        db_object.execute(f'UPDATE users SET is_subscriber = true WHERE id ={user_id};')
        db_connection.commit()
        return text.you_are_subscribed_message
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return text.something_goes_wrong(error=error)


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
    db_object.execute(f'UPDATE users SET is_admin = true WHERE id ={user_id};')
    db_connection.commit()


# Making messages
# ToDo make more 1 row with title
async def new_post(user_id: int, post_text: str):
    db_object.execute(f"INSERT INTO posts (author_id,text) VALUES ('{user_id}','{post_text}')")
    db_connection.commit()


# TODO - шедуле
async def send_post(user_id: int):
    # Получение всех подписчиков
    db_object.execute(f"SELECT id from users where is_subscriber=true")
    subscribers = db_object.fetchall()
    # Получение последнего сообщения от человека с user_id
    db_object.execute(f"SELECT text from posts where author_id={user_id} order by posts.date_creation desc ")
    post = db_object.fetchone()[0]
    # debug
    logger.debug(post)
    logger.debug(subscribers)
    # sending messages
    operator = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
    for subscriber in subscribers:
        logger.debug(subscriber[0])
        await operator.send_message(str(subscriber[0]), post)
        await asyncio.sleep(5)
    await operator.close()


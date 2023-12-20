import asyncio
import re

import psycopg2
from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger

from app import config
from app.utils.data import db_text as text

class Database:
    connection = None
    object = None

    # DB for user
    # Сохраняем текущее «состояние» пользователя в нашу базу
    def create_user(self, user_id: int):
        try:
            self.object.execute(f"SELECT id FROM users WHERE id  = {user_id}")
            result = self.object.fetchone()
            if result is None:
                logger.info(f"Creating user {user_id}")
                self.object.execute(f"INSERT INTO users (id) VALUES ('{user_id}')")
                self.connection.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return False

    # Получаем текущее состояние пользователя
    def get_user(self, user_id: int):
        try:
            self.object.execute(f"SELECT * from users where id={user_id}")
            result = self.object.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)

    def set_subscribe_to_newsletter(self, user_id: int):
        try:
            self.object.execute(f'UPDATE users SET is_subscriber = true WHERE id ={user_id};')
            self.connection.commit()
            return text.you_are_subscribed_message
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)

    def does_user_subscribe_to_newsletter(self, user_id: int):
        self.object.execute(f"SELECT * from users where id={user_id}")
        user = self.object.fetchall()
        return user[0][1]

    # DB for admin
    def does_user_admin(self, user_id: int):
        self.create_user(user_id)
        self.object.execute(f"SELECT * from users where id={user_id}")
        user = self.object.fetchall()
        return user[0][2]

    def set_user_to_admin(self, user_id: str):
        logger.info(f"New admin is {user_id}")
        self.object.execute(f'UPDATE users SET is_admin = true WHERE id ={user_id};')
        self.connection.commit()

    # Making messages
    # ToDo make more 1 row with title
    async def new_post(self, user_id: int, post_text: str):
        logger.info(f"Creating new post from {user_id} and post {post_text}")
        self.object.execute(f"INSERT INTO posts (author_id,text) VALUES ('{user_id}','{post_text}')")
        self.connection.commit()

    # TODO - шедуле
    async def send_post(self, user_id: int):
        logger.info(f"Sending post from {user_id}")
        # Получение всех подписчиков
        self.object.execute(f"SELECT id from users where is_subscriber=true")
        subscribers = self.object.fetchall()
        logger.info(f"All subscribers: {subscribers}")
        # Получение последнего сообщения от человека с user_id
        self.object.execute(f"SELECT text from posts where author_id={user_id} order by posts.date_creation desc ")
        post = self.object.fetchone()[0]
        # debug
        logger.info(f"Sending post is: {post}")
        logger.info(f"All subscribers: {subscribers}")
        # sending messages
        operator = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
        for subscriber in subscribers:
            logger.info(subscriber[0])
            await operator.send_message(str(subscriber[0]), post)
            await asyncio.sleep(5)
        await operator.close()

db = Database()

def start_up():
    if db.connection is None:
        try:
            db.connection = psycopg2.connect(config.POSTGRES_URI, sslmode="disable")
            db.object = db.connection.cursor()
            logger.info("Connected to database")
        except Exception as error:
            logger.error("Error: Connection not established {}".format(error))
    else:
        logger.error("Connection established")

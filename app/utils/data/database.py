import re

import psycopg2
from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger
from pydantic import ValidationError

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
            return text.something_goes_wrong(error=error)


    def set_subscribe_to_newsletter(self, user_id: int):
        try:
            self.object.execute(f'UPDATE users SET is_subscriber = true WHERE id ={user_id};')
            self.connection.commit()
            return text.you_are_subscribed_message
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return text.something_goes_wrong(error=error)


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
        try:
            self.object.execute(f'UPDATE users SET is_admin = true WHERE id ={user_id};')
            self.connection.commit()
            return text.new_one_admin_message
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return text.something_goes_wrong(error=error)


    # Making messages
    # ToDo make more 1 row with title
    def new_post(self, user_id: int, post_text: str):
        try:
            self.object.execute(f"INSERT INTO posts (author_id,text) VALUES ('{user_id}','{post_text}')")
            self.connection.commit()
            return post_text
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return text.something_goes_wrong(error=error)


    # TODO - шедуле
    async def send_post(self):
        # Получение всех подписчиков
        try:
            Database.object.execute(f"SELECT id from users where is_subscriber=true")
            subscribers = Database.object.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return text.something_goes_wrong(error=error)
        try:
            Database.object.execute(f"SELECT id from users where is_subscriber=true")
            # post = Database.object.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            return text.something_goes_wrong(error=error)

        try:
            if config.USER_BOT_TOKEN is not None:
                operator = Bot(config.USER_BOT_TOKEN, parse_mode=ParseMode.HTML)
                for subscriber in subscribers:
                    subscriber_id = re.findall("\d+", str(subscriber))[0]
                    logger.info(subscriber_id)
                    await operator.send_message(chat_id=int(subscriber_id), text='Проверка', parse_mode=ParseMode.HTML)
                await operator.close()
            else:
                raise Exception(text.user_bot_token_exception)
        except ValidationError as error:
            text.something_goes_wrong(error=error)

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

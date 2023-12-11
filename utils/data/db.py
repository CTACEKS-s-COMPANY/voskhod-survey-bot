import psycopg2

import config

db_connection = psycopg2.connect(config.POSTGRES_URI, sslmode="disable")
db_object = db_connection.cursor()


# Сохраняем текущее «состояние» пользователя в нашу базу
def create_user(user_id: int):
    db_object.execute(f"INSERT INTO users (id) VALUES ('{user_id}')")
    db_connection.commit()


# Получаем текущее состояние пользователя
async def get_users():
    db_object.execute(f"SELECT * from users")
    result = db_object.fetchall()
    return str(result)

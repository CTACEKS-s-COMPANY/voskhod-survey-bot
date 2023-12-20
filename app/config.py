import os

from dotenv import load_dotenv

load_dotenv()

USER_BOT_TOKEN = os.getenv("USER_BOT_TOKEN")

# @voskhod_survey_admin_bot
ADMIN_BOT_ID = os.getenv("ADMIN_BOT_TOKEN")

POSTGRES_DB = str(os.getenv('POSTGRES_DB'))

POSTGRES_USER = str(os.getenv('POSTGRES_USER'))

POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))

POSTGRES_HOST = str(os.getenv('POSTGRES_HOST'))

POSTGRES_PORT = 5432

POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

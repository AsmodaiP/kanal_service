import os

from dotenv import load_dotenv

load_dotenv()

PATH_TO_LOGS = os.getenv('PATH_TO_LOGS', 'logs')
CURRENCY_CODE = os.getenv('CURRENCY_CODE', 'R01235')

PG_USERNAME = os.getenv('PG_USERNAME', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'admin')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DATABASE = os.getenv('PG_DATABASE', 'test')
DATABASE_URL = f'postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATETIME_FORMAT = os.getenv('DATETIME_FORMAT', '%d.%m.%Y')
CHAT_ID_FOR_NOTIFICATION = os.getenv('CHAT_ID_FOR_NOTIFICATION', '%d.%m.%Y')

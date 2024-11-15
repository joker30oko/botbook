from os import environ

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

load_dotenv()

token = environ.get('BOT_TOKEN')
group_id = environ.get('GROUP_ID')
secret_group_id = environ.get('SECRET_GROUP_ID')
api_key = environ.get('API_KEY')

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())
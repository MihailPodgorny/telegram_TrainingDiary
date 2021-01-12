import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

# token from .env file
API_TOKEN = os.getenv("API_TOKEN_TELEGRAM")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветствие и помощь"""
    await message.answer("Hello!")


@dp.message_handler(commands=['new'])
async def today_statistics(message: types.Message):
    pass
    await message.answer(answer_message)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from workouts import Workouts, MusclesGroups

load_dotenv()
# Get token from .env file.
API_TOKEN = os.getenv("API_TOKEN_TELEGRAM")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Get groups of muscles for choice of workout type.
muscles_groups = '\n'.join(tuple(str(group.get('group_name')) for group in MusclesGroups.load_groups()))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Send greeting and help"""
    await message.answer("Hello!")


@dp.message_handler(commands=['new'])
async def today_statistics(message: types.Message):
    """Add new workout"""
    new_workout = Workouts(message.from_user.id)
    new_workout.add_new_workout()

    answer_message = f"Добавлена новая тренировка\nВыберите группу мышц\n{muscles_groups}"
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

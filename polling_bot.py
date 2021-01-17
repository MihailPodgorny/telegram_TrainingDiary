import logging
import os
import re

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import services
from workouts import Workouts, MusclesGroups, Exercises, Users, Sets

load_dotenv()
# Get token from .env file.
API_TOKEN = os.getenv("API_TOKEN_TELEGRAM")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Get groups of muscles for choice of workout type.
muscles_groups = MusclesGroups.load_groups()
muscles_group_names = list(group.get('group_name') for group in muscles_groups)
muscles_group_id = list(group.get('group_id') for group in muscles_groups)

# Get all exercises for handler
all_exercises = Exercises.load_all_exercises()
all_exercises_names = list(ex.get('exercise_name') for ex in all_exercises)
all_exercises_id = list(ex.get('exercise_id') for ex in all_exercises)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Send greeting and help"""
    await message.answer("Приветствую в тренировочном дневнике!")


@dp.message_handler(commands=['new'])
async def today_statistics(message: types.Message):
    """Add new workout and new user if not exist"""
    user_id = message.from_user.id
    user_ids = services.get_all_user_ids()
    if user_id not in user_ids:
        user = Users(user_id)
        user.add_new_user()

    new_workout = Workouts(user_id)
    new_workout.add_new_workout()

    markup = services.generate_markup(muscles_group_names)
    answer_message = f"Добавлена новая тренировка\nВыберите группу мышц"
    await message.answer(answer_message, reply_markup=markup)


@dp.message_handler(commands=muscles_group_names)
async def send_welcome(message: types.Message):
    group_name = message.text[1:]
    group_id = muscles_group_id[muscles_group_names.index(group_name)]
    exercise_names = services.generate_next_exercise(int(group_id))
    markup = services.generate_markup(exercise_names)
    await message.answer(f"Ну ок, {group_name}. Укажите упражение.", reply_markup=markup)


@dp.message_handler(commands=all_exercises_names)
async def send_welcome(message: types.Message):
    exercise_name = message.text[1:]
    exc = Exercises()
    exc_id = [ex.get('exercise_id') for ex in exc.get_exercise_by_name(exercise_name)][0]
    # меняем статус пользователя на текущее упражнение
    Users.set_user_status(message.from_user.id, exc_id)
    await message.answer(f"Погнали! Необходимо указать вес и число повторений.")


@dp.message_handler(commands=['next'])
async def send_welcome(message: types.Message):
    user = Users.get_user_params(message.from_user.id)
    user_status = user[0].get('status')
    exc = Exercises()
    group_id = [ex.get('group_id') for ex in exc.get_exercise_by_id(user_status)][0]
    exercise_names = services.generate_next_exercise(int(group_id))
    markup = services.generate_markup(exercise_names)
    await message.answer("Ок, выберите следующее упражнение", reply_markup=markup)


@dp.message_handler(regexp=r"^\s*(\d+)\s*(\d*)\s*")
async def send_welcome(message: types.Message):
    regexp_result = re.match(r"^\s*(\d+)\s*(\d*)\s*", message.text)
    weight = regexp_result.group(1)
    reps = regexp_result.group(2)
    # id упражениния равно текущему статусу пользователя
    user_id = message.from_user.id
    user = Users.get_user_params(user_id)
    exercise_id = user[0].get('status')
    print(f"вес={weight}, повторы = {reps}.")
    if not reps.isdigit():
        reps = weight
        weight = user[0].get('load')
    Sets(user_id, exercise_id, weight, reps)
    Users.set_user_load(message.from_user.id, weight)
    await message.answer(f"Добавлено: {weight} кг на {reps} повт.")


@dp.message_handler(commands=['end'])
async def send_welcome(message: types.Message):
    # TODO сделать обновление полей времени в Exercise
    Users.set_user_status(message.from_user.id, 0)
    await message.answer("Отлично потренировались!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

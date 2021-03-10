import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import utils

load_dotenv()
# Get token from .env file.
API_TOKEN = os.getenv("API_TOKEN_TELEGRAM")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
utils.for_new_db()

HELP_TEXT = "Бот предназначен для ведения личного дневника тренировок,\n" \
            "что является одним из столпов в прогрессии роста результата.\n" \
            "Перечень команд:\n" \
            "/new - для начала новой тренировки:\n" \
            "после выбора группы мышц и упражнения, следует указать вес и повторения;\n" \
            "например: 80 12\n" \
            "/next - для выбора следующего упражнения;\n" \
            "/end - закончить тренировку и сохранить статистику;\n" \
            "/help - для вызова помощи."

MUSCLE_GROUPS = utils.get_all_muscle_groups()
ALL_EXERCISES = utils.get_all_exercises()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Send greeting and help"""
    await message.answer(f"Приветствую в тренировочном дневнике!\n {HELP_TEXT}")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """Send help"""
    await message.answer(HELP_TEXT)


@dp.message_handler(commands=['new'])
async def today_statistics(message: types.Message):
    """ Add new workout and new user if not exist """
    chat_id = message.from_user.id
    if utils.is_user_exist(chat_id):
        utils.nullify_user(chat_id)
    else:
        utils.create_new_user(chat_id)
    utils.create_new_workout(chat_id)
    markup = utils.generate_markup(MUSCLE_GROUPS)
    answer_message = f"Добавлена новая тренировка.\nВыберите группу мышц:"
    await message.answer(answer_message, reply_markup=markup)


@dp.message_handler(commands=MUSCLE_GROUPS)
async def send_welcome(message: types.Message):
    """ Choose exercise in group """
    """ """
    group_name = message.text[1:]
    exercises = utils.get_all_exercises_by_group_name(group_name)
    markup = utils.generate_markup(exercises)
    await message.answer(f"Хорошо, сегодня {group_name}. Выберите упражнение:", reply_markup=markup)


@dp.message_handler(commands=ALL_EXERCISES)
async def send_welcome(message: types.Message):
    """ Get exercise name, set User.state = Exercise.id """
    exercise_name = message.text[1:]
    user_chat = message.from_user.id
    exercise_id = utils.get_exercises_by_name(exercise_name)
    utils.set_user_state(user_chat, exercise_id)
    await message.answer(f"Погнали! Необходимо указать вес и число повторений.\n"
                         "/next - для следующего упражнения")


@dp.message_handler(commands=['next'])
async def send_welcome(message: types.Message):
    """ Get user state and add new exercise """
    user_chat = message.from_user.id
    user_state = utils.get_user_state(user_chat)
    if user_state == 0:
        await message.answer("Похоже, Вы забыли добавить новую тренировку через /new")
    else:
        exercise_id = user_state
        group_id = utils.get_group_id_by_exercise_id(exercise_id)
        exercise_names = utils.get_all_exercises_by_group_id(group_id)
        markup = utils.generate_markup(exercise_names)
        await message.answer("Ок, выберите следующее упражнение:", reply_markup=markup)


# TODO добавить скрытие клавиатуры
# TODO при вводе показывать статистику по упражнению в сравнении с прошлой тренировкой
@dp.message_handler(regexp=r"^\s*(\d+)\s*(\d*)\s*")
async def send_welcome(message: types.Message):
    """
    Get text message from user, get weight (arg_1) and reps(arg_2) from message.
    If arg_2 is empty then reps = arg_2 and weight = User.load
    Add new exercise set.
    """
    chat_id = message.from_user.id
    if not utils.is_user_exist(chat_id):
        await message.answer(f"Похоже, Вы новый пользователь!\n"
                             f"Начните новую тренировку через /new")
    exercise_id = utils.get_user_state(chat_id)
    if exercise_id == 0:
        await message.answer(f"Пожалуйста, выберите упражнение!\n")

    arg_1, arg_2 = utils.get_weight_and_reps_from_message(message.text)
    if arg_2.isdigit():
        weight, reps = arg_1, arg_2
    else:
        reps = arg_1
        weight = utils.get_user_load(chat_id)

    utils.create_new_set(chat_id, exercise_id, weight, reps)
    utils.set_user_state_and_load(chat_id, exercise_id, weight)
    await message.answer(f"Добавлено: {weight} кг на {reps} повт.")


# TODO добавить скрытие клавиатуры
@dp.message_handler(commands=['end'])
async def send_welcome(message: types.Message):
    """ Nullify user.status and user.load, then update workout.time_end and total time """
    chat_id = message.from_user.id
    utils.nullify_user(chat_id)
    utils.set_workout_end_time(chat_id)
    await message.answer("Отлично потренировались!")


# TODO добавить модуль статистики по тренировке /stat
# TODO /delete для удаления последнего подхода
# TODO /group для другой группы мышц
# TODO фильтр для перехвата флуда


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

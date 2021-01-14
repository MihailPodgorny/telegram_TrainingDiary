from typing import Dict, List

from aiogram import types

from workouts import Exercises, Users


def generate_markup(buttons: List):
    """Create keyboard"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons:
        markup.add('/'+str(button))
    return markup


def generate_next_exercise(group_id: int):
    ex = Exercises(group_id)
    exercises = ex.get_exercises()
    exercise_names = list(str(name.get('exercise_name')) for name in exercises)
    return exercise_names


def get_all_user_ids():
    users = Users.load_all_users()
    user_ids = list(user.get('user_id') for user in users)
    return user_ids

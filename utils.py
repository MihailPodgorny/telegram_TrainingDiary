import re
from datetime import datetime
from typing import List

from aiogram import types

from db import get_all_data, get_all_data_by_group_id, update_user_state_and_load_by_chat_id, create, \
    get_user_id_by_chat, get_id_by_name, get_by_id, get_user_state_by_chat, get_user_load_by_chat, \
    get_last_workout, update_workout_by_id, get_count, delete, get_last_set
from models import Users, Exercises, MuscleGroups, Workouts, Sets
from start_data import create_start_data


def generate_markup(buttons: List):
    """ create keyboard in Telegram """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons:
        markup.add('/'+str(button))
    return markup


def is_user_exist(chat_id: int):
    """ get all chat ID in DB and find particular user chat_id """
    all_data = get_all_data(Users)
    all_chat_id = []
    for row in all_data:
        all_chat_id.append(row.chat)
    return True if chat_id in all_chat_id else False


def get_user_state(chat_id: int):
    """ get user state """
    user_state = get_user_state_by_chat(Users, chat_id)
    return user_state


def get_user_load(chat_id: int):
    """ get user load """
    user_load = get_user_load_by_chat(Users, chat_id)
    return user_load


def get_weight_and_reps_from_message(text: str):
    """get weight and reps in text message"""
    regexp_result = re.match(r"^\s*(\d+)\s*(\d*)\s*", text)
    weight = regexp_result.group(1)
    reps = regexp_result.group(2)
    return weight, reps


def get_all_exercises_by_group_id(group_id: int):
    """ get all exercises particular group_id """
    all_data = get_all_data_by_group_id(Exercises, group_id)
    all_exercises = []
    for exs in all_data:
        all_exercises.append(exs.name)
    return all_exercises


def get_all_exercises_by_group_name(group_name: str):
    group_id = get_id_by_name(MuscleGroups, group_name)
    return get_all_exercises_by_group_id(group_id)


def get_exercises_by_name(exercise_name: str):
    return get_id_by_name(Exercises, exercise_name)


def get_all_exercise_data(exercise_id: int):
    exs = get_by_id(Exercises, exercise_id)
    return exs.name, exs.group_id, exs.original_name, exs.similar_name, exs.video_href


def get_group_id_by_exercise_id(exercise_id: int):
    exs = get_by_id(Exercises, exercise_id)
    return exs.group_id


def get_last_workout_id_by_user_id(user_id: int):
    last_workout, date_now, start_time = get_last_workout(Workouts, user_id)
    return last_workout


def get_last_set_id_by_workout_id(workout_id: int):
    last_set_id, _, last_exercise_id, last_weight, _ = get_last_set(Sets, workout_id)
    return last_set_id, last_exercise_id, last_weight


def get_all_muscle_groups():
    all_data = get_all_data(MuscleGroups)
    all_groups = []
    for row in all_data:
        all_groups.append(row.name)
    return all_groups


def get_all_exercises():
    """ get all exercises in database """
    all_data = get_all_data(Exercises)
    all_exercises = []
    for row in all_data:
        all_exercises.append(row.name)
    return all_exercises


def nullify_user(chat_id: int):
    """ update user with param state=0 and load=0 """
    update_user_state_and_load_by_chat_id(Users, chat_id, 0, 0)


def set_user_state(chat_id: int, state: int):
    """ update user with param state and load=0 """
    update_user_state_and_load_by_chat_id(Users, chat_id, state, 0)


def set_user_state_and_load(chat_id: int, state: int, load: int):
    """ update user with param state and load """
    update_user_state_and_load_by_chat_id(Users, chat_id, state, load)


def set_workout_end_time(chat_id: int):
    """ update end_time and total_time in Workout """
    user_id = get_user_id_by_chat(Users, chat_id)
    workout_id, date_, time_ = get_last_workout(Workouts, user_id)
    start_date = datetime.combine(date_, time_)
    end_date = datetime.now()
    end_time = datetime.time(end_date)
    total_time = (end_date - start_date).total_seconds() // 60
    update_workout_by_id(Workouts, workout_id, end_time, total_time)


def create_new_user(chat_id: int):
    """ create new user """
    create(Users(chat=chat_id))


def create_new_workout(chat_id: int):
    """ create new workout """
    user_id = get_user_id_by_chat(Users, chat_id)
    print(user_id)
    create(Workouts(user_id=user_id))


def create_new_set(chat_id: int, exercise_id: int, weight, reps):
    """ create new set """
    user_id = get_user_id_by_chat(Users, chat_id)
    workout_id = get_last_workout_id_by_user_id(user_id)
    create(Sets(workout_id=workout_id,
                exercise_id=exercise_id,
                weight=weight,
                reps=reps))


def for_new_db():
    if get_count(MuscleGroups) == 0:
        create_start_data()


def delete_user(chat_id: int):
    user_id = get_user_id_by_chat(Users, chat_id)
    delete(Users, user_id)


def delete_set(chat_id: int):
    user_id = get_user_id_by_chat(Users, chat_id)
    workout_id = get_last_workout_id_by_user_id(user_id) or None
    if workout_id:
        last_set_id, last_exercise_id, _ = get_last_set_id_by_workout_id(workout_id)
        if last_set_id:
            delete(Sets, last_set_id)
            prev_workout_id = get_last_workout_id_by_user_id(user_id) or None
            if prev_workout_id:
                prev_set_id, prev_exercise_id, prev_weight = get_last_set_id_by_workout_id(workout_id)
                set_user_state_and_load(chat_id, prev_exercise_id, prev_weight)
            else:
                nullify_user(chat_id)

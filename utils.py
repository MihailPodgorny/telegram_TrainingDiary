import re
import json
from datetime import datetime
from typing import List

from aiogram import types

from db.db import get_all_data, get_all_data_by_group_id, update_user_state_and_load_by_chat_id, create, \
    get_user_id_by_chat, get_id_by_name, get_by_id, get_user_state_by_chat, get_user_load_by_chat, \
    get_last_workout, update_workout_by_id, get_count, delete, get_last_set, get_all_data_by_workout_id
from db.models import Users, Exercises, MuscleGroups, Workouts, Sets

INITIAL_DATA_FILE = 'db/starting_data.json'


def generate_markup(buttons: List):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons:
        markup.add('/' + str(button))
    return markup


def is_user_exist(chat_id: int):
    all_data = get_all_data(Users)
    for row in all_data:
        if row.chat == chat_id:
            return True
    return False


def is_workout_exist(chat_id: int):
    user_id = get_user_id_by_chat(Users, chat_id)
    last_workout = get_last_workout_id_by_user_id(user_id) or None
    if not last_workout:
        return False
    return True


def are_user_and_workout_exist(chat_id: int):
    return True if is_user_exist(chat_id) and is_workout_exist(chat_id) \
        else False


def create_new_user(chat_id: int):
    create(Users(chat=chat_id))


def create_new_workout(chat_id: int):
    user_id = get_user_id_by_chat(Users, chat_id)
    create(Workouts(user_id=user_id))


def create_new_set(chat_id: int, exercise_id: int, weight, reps):
    user_id = get_user_id_by_chat(Users, chat_id)
    workout_id = get_last_workout_id_by_user_id(user_id)
    create(Sets(workout_id=workout_id,
                exercise_id=exercise_id,
                weight=weight,
                reps=reps))


def get_user_state(chat_id: int):
    user_state = get_user_state_by_chat(Users, chat_id)
    return user_state


def get_user_load(chat_id: int):
    user_load = get_user_load_by_chat(Users, chat_id)
    return user_load


def get_weight_and_reps_from_message(text: str):
    regexp_result = re.match(r"^\s*(\d+)\s*(\d*)\s*", text)
    weight = regexp_result.group(1)
    reps = regexp_result.group(2)
    return weight, reps


def get_all_exercises_by_group_id(group_id: int):
    all_data = get_all_data_by_group_id(Exercises, group_id)
    all_exercises = []
    for exs in all_data:
        all_exercises.append(exs.name)
    return all_exercises


def get_all_sets_by_workout_id(workout_id: int):
    all_data = get_all_data_by_workout_id(Sets, workout_id)
    all_sets = {}
    for _set in all_data:
        exs = get_by_id(Exercises, _set.exercise_id)
        all_sets.update({exs.name: [
            {'weigth': _set.weight,
             'reps': _set.reps}
        ]})
    return all_sets


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
    all_data = get_all_data(Exercises)
    all_exercises = []
    for row in all_data:
        all_exercises.append(row.name)
    return all_exercises


def set_user_state_and_load(chat_id: int, state: int, load: int):
    update_user_state_and_load_by_chat_id(Users, chat_id, state, load)


def set_user_state(chat_id: int, state: int):
    update_user_state_and_load_by_chat_id(Users, chat_id, state, 0)


def nullify_user(chat_id: int):
    update_user_state_and_load_by_chat_id(Users, chat_id, 0, 0)


def set_workout_end_time(chat_id: int):
    user_id = get_user_id_by_chat(Users, chat_id)
    workout_id, date_, time_ = get_last_workout(Workouts, user_id)
    start_date = datetime.combine(date_, time_)
    end_date = datetime.now()
    end_time = datetime.time(end_date)
    total_time = (end_date - start_date).total_seconds() // 60
    update_workout_by_id(Workouts, workout_id, end_time, total_time)


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


def is_new_db():
    if not get_count(MuscleGroups):
        with open(INITIAL_DATA_FILE) as file:
            data = json.load(file)
        # TODO сделать валидацию данных
        for table_name in data:
            for row in data[table_name]:
                if table_name == 'MuscleGroups':
                    create(MuscleGroups(name=row.get('name', 'еще одна группа мышщ'),
                                        text_href=row.get('text_href', '')))
                elif table_name == 'Exercises':
                    create(Exercises(name=row.get('name', 'еще одно упражение'),
                                     group_id=get_id_by_name(MuscleGroups, row.get('group', 'прочее')) \
                                              or get_id_by_name(MuscleGroups, 'прочее'),
                                     original_name=row.get('original_name', 'еще одно упражение'),
                                     similar_name=row.get('similar_name', ''),
                                     video_href=row.get('video_href', '')))
        return 'Initial data has loaded'
    return 'Initial data was loaded earlier'

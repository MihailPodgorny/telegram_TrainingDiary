from datetime import datetime

import pytest


from db.db import get_user_id_by_chat, get_by_id, get_user_state_by_chat, get_user_load_by_chat, \
    update_user_state_and_load_by_chat_id, get_id_by_name, get_all_data, get_last_workout, update_workout_by_id, \
    get_last_set, get_all_data_by_workout_id
from db.models import Users, Exercises, MuscleGroups, Workouts, Sets
from tests.conftest import USER_CHAT, USER_STATE, USER_LOAD, WEIGHT, REPS


def test_users(create_data):
    user_id = get_user_id_by_chat(Users, chat=USER_CHAT)
    assert isinstance(user_id, int)
    user = get_by_id(Users, pk=user_id)
    assert isinstance(user, Users)
    assert user.chat == USER_CHAT
    user_state = get_user_state_by_chat(Users, USER_CHAT)
    assert user_state == USER_STATE
    user_load = get_user_load_by_chat(Users, USER_CHAT)
    assert user_load == USER_LOAD
    new_state_n_load = (1, 100)
    update_user_state_and_load_by_chat_id(Users, USER_CHAT, new_state_n_load[0], new_state_n_load[1])
    user_state = get_user_state_by_chat(Users, USER_CHAT)
    user_load = get_user_load_by_chat(Users, USER_CHAT)
    assert (user_state, user_load) == new_state_n_load


def test_exercises():
    exc_id = get_id_by_name(MuscleGroups, 'грудные')
    exc_id = 1
    query = get_all_data(MuscleGroups)
    assert query is not None


def test_workouts(create_data):
    user_id = get_user_id_by_chat(Users, chat=USER_CHAT)
    workout_id, workout_date_now, workout_start_time = get_last_workout(Workouts, user_id)
    workout = get_by_id(Workouts, workout_id)
    assert workout_id == workout.id
    assert workout.total_time == 0
    prev_workout_end_time = workout.end_time
    end_time = datetime.time(datetime.now())
    total_time = 45
    update_workout_by_id(Workouts, workout_id, end_time, total_time)
    workout = get_by_id(Workouts, workout_id)
    assert prev_workout_end_time != workout.end_time
    assert workout.total_time == 45


def test_sets(create_data):
    user_id = get_user_id_by_chat(Users, chat=USER_CHAT)
    workout_id, date_now, total_time = get_last_workout(Workouts, user_id)
    set_id, workout_id, exercise_id, weight, reps = get_last_set(Sets, workout_id)
    assert weight == WEIGHT
    assert reps == REPS
    raw_data = get_all_data_by_workout_id(Sets, workout_id)
    all_sets = []
    for _set in raw_data:
        all_sets.append(f"{_set.weight} {_set.reps}")
    assert len(all_sets) == 2

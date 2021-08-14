import pytest

from tests.conftest import USER_CHAT
from utils import is_user_exist, get_user_state, set_user_state, get_user_load, set_user_state_and_load, \
    nullify_user, get_weight_and_reps_from_message, is_workout_exist, are_user_and_workout_exist, create_new_user, \
    create_new_workout, create_new_set, is_set_exist


@pytest.mark.parametrize('message, expected_load_n_reps',
                         [('80 12', ('80', '12',)),
                          ('15', ('15', '',))])
def test_message(message, expected_load_n_reps):
    loads, reps = get_weight_and_reps_from_message(message)
    assert (loads, reps) == expected_load_n_reps


def test_is_user_exist(create_data):
    assert is_user_exist(USER_CHAT)
    assert not is_user_exist(999999)


def test_is_workout_exist(create_data):
    assert is_workout_exist(USER_CHAT)
    pass


@pytest.mark.xfail
def test_is_not__workout_exist():
    assert not is_workout_exist(999999)


def test_are_user_and_workout_exist(create_data):
    assert are_user_and_workout_exist(USER_CHAT)
    assert not are_user_and_workout_exist(999999)


def test_is_set_exist(create_data):
    assert is_set_exist(USER_CHAT)
    assert not is_set_exist(999999)


def test_create_new_user():
    new_user_id = 77777
    create_new_user(new_user_id)
    assert is_user_exist(new_user_id)


def test_create_new_workout():
    new_user_id = 77777
    create_new_workout(new_user_id)
    assert is_workout_exist(new_user_id)


def test_create_new_set():
    new_user_id = 77777
    exercise_id = 1
    weight = 80
    reps = 12
    create_new_set(new_user_id, exercise_id, weight, reps)
    pass


@pytest.mark.parametrize('state',
                         [4,
                          2])
def test_get_and_set_user_state(create_data, state):
    set_user_state(USER_CHAT, state)
    assert get_user_state(USER_CHAT) == state


@pytest.mark.parametrize('state, load',
                         [(4, 50),
                          (2, 100)])
def test_get_and_set_user_load(create_data, state, load):
    set_user_state_and_load(USER_CHAT, state, load)
    assert get_user_state(USER_CHAT) == state
    assert get_user_load(USER_CHAT) == load
    nullify_user(USER_CHAT)
    assert get_user_state(USER_CHAT) == 0
    assert get_user_load(USER_CHAT) == 0

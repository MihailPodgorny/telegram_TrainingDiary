import pytest

from tests.conftest import USER_CHAT
from utils import is_user_exist, get_user_state, set_user_state, get_user_load,set_user_state_and_load, \
    nullify_user, get_weight_and_reps_from_message


@pytest.mark.parametrize('message, expected_load_n_reps',
                         [('80 12', ('80', '12',)),
                          ('15', ('15', '',))])
def test_message(message, expected_load_n_reps):
    loads, reps = get_weight_and_reps_from_message(message)
    assert (loads, reps) == expected_load_n_reps


def test_is_user_exist():
    assert is_user_exist(USER_CHAT)
    assert not is_user_exist(999999)


@pytest.mark.parametrize('state',
                         [4,
                          2])
def test_get_and_set_user_state(state):
    set_user_state(USER_CHAT, state)
    assert get_user_state(USER_CHAT) == state


@pytest.mark.parametrize('state, load',
                         [(4, 50),
                          (2, 100)])
def test_get_and_set_user_load(create_user, state, load):
    set_user_state_and_load(USER_CHAT, state, load)
    assert get_user_state(USER_CHAT) == state
    assert get_user_load(USER_CHAT) == load
    nullify_user(USER_CHAT)
    assert get_user_state(USER_CHAT) == 0
    assert get_user_load(USER_CHAT) == 0

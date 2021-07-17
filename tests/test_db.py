from db.db import get_user_id_by_chat, get_by_id, get_user_state_by_chat, get_user_load_by_chat, \
    update_user_state_and_load_by_chat_id
from db.models import Users
from tests.conftest import USER_CHAT, USER_STATE, USER_LOAD


def test_user(create_user):
    user_chat = USER_CHAT
    user_id = get_user_id_by_chat(Users, chat=user_chat)
    assert isinstance(user_id, int)
    user = get_by_id(Users, pk=user_id)
    assert isinstance(user, Users)
    assert user.chat == user_chat
    user_state = get_user_state_by_chat(Users, user_chat)
    assert user_state == USER_STATE
    user_load = get_user_load_by_chat(Users, user_chat)
    assert user_load == USER_LOAD
    new_state_n_load = (1, 100)
    update_user_state_and_load_by_chat_id(Users, user_chat, new_state_n_load[0], new_state_n_load[1])
    user_state = get_user_state_by_chat(Users, user_chat)
    user_load = get_user_load_by_chat(Users, user_chat)
    assert (user_state, user_load) == new_state_n_load


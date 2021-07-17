import pytest
from db.db import create, delete
from db.models import Users

STARTING_DATA_JSON_FILE = 'starting_data.json'
USER_CHAT = 999
USER_STATE = 0
USER_LOAD = 80
GROUP_ID = 2


@pytest.fixture(scope='session')
def create_user():
    model_id = create(Users(chat=USER_CHAT, state=USER_STATE, load=USER_LOAD))
    yield 'User created'
    delete(Users, model_id)

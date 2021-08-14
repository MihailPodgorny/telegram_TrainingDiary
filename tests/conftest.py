import pytest
from db.db import create, delete
from db.models import Users, Workouts, Sets

STARTING_DATA_JSON_FILE = 'starting_data.json'
USER_CHAT = 999
USER_STATE = 0
USER_LOAD = 80
GROUP_ID = 2
WEIGHT = 80
REPS = 8


@pytest.fixture(scope='session')
def create_data():
    user_id = create(Users(chat=USER_CHAT, state=USER_STATE, load=USER_LOAD))
    workout1_id = create(Workouts(user_id=user_id))
    workout2_id = create(Workouts(user_id=user_id))
    set1_id = create(Sets(workout_id=workout1_id, exercise_id=1, weight=60, reps=12))
    set2_id = create(Sets(workout_id=workout1_id, exercise_id=2, weight=50, reps=15))
    workout2_id = create(Workouts(user_id=user_id))
    set3_id = create(Sets(workout_id=workout2_id, exercise_id=1, weight=70, reps=6))
    set4_id = create(Sets(workout_id=workout2_id, exercise_id=2, weight=WEIGHT, reps=REPS))


    yield 'Data created'
    delete(Users, user_id)
    delete(Workouts, workout1_id)
    delete(Workouts, workout2_id)
    delete(Sets, set1_id)
    delete(Sets, set2_id)

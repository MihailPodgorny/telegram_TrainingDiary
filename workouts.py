from datetime import datetime, timedelta
from typing import NamedTuple
from uuid import uuid4


import db


class Workout(NamedTuple):
    """Описание объекта Тренировка"""
    workout_id: str
    user_id: int
    date_: str
    start_time: str
    end_time: str
    total_time: int


class Workouts:
    def __init__(self, user_id):
        self.workout_id = str(uuid4())
        self.user_id = user_id
        self.date_ = datetime.now().strftime('%Y.%m.%d ')
        self.start_time = datetime.now().strftime('%H:%M')
        self.end_time = (datetime.now()+timedelta(minutes=2)).strftime('%H:%M')
        self.total_time = 0
        self.workout = Workout(self.workout_id,
                               self.user_id,
                               self.date_,
                               self.start_time,
                               self.end_time,
                               self.total_time)
        self.columns = self.workout.__dir__()

    def __str__(self):
        return f"Workout: {self.workout_id}"

    def __repr__(self):
        return f"Workout: {self.workout_id}"

    def add_new_workout(self):
        db.insert("workouts", self.workout._asdict())


class Exercise(NamedTuple):
    """Описание объекта Упражнение"""
    exercise_id: str
    name: str
    group_id: int
    english_name: str
    video: str


class Exercises:
    pass


class MusclesGroup:
    """Описание объекта Группа мышц"""
    group_id: int
    group_name: str
    href: str


class MusclesGroups:
    @staticmethod
    def load_groups():
        groups = db.fetchall("groups", ["group_name"])
        return groups


class OneSet(NamedTuple):
    """Описание объекта Подход"""
    set_id: str
    workout_id: int
    exercise_id: int
    weight: int
    reps: int


class Sets:
    def __init__(self, workout_id, exercise_id):
        self.set_id = str(uuid4())
        self.workout_id = workout_id
        self.exercise_id = exercise_id
        self.weight = 0
        self.reps = 0
        self.set = OneSet(self.set_id,
                          self.workout_id,
                          self.exercise_id,
                          self.weight,
                          self.reps)

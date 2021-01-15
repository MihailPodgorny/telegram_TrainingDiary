from datetime import datetime, timedelta
from typing import NamedTuple
from uuid import uuid4


import db


class User(NamedTuple):
    """
    Описание объекта Пользователь. Пользователь может находиться в состоянии 0 или
    в состоянии, равном идентификатору упражнения.
    """
    user_id: int
    status: int


class Users:
    def __init__(self, user_id, status=0):
        self.user = User(user_id, status)

    def add_new_user(self):
        db.insert("users", self.user._asdict())

    @staticmethod
    def get_user_status(user_id):
        return db.filtered_select("users", ["status"], "user_id", user_id)

    @staticmethod
    def set_user_status(user_id, new_status):
        db.update_one("users", "status", new_status, "user_id", user_id)

    @staticmethod
    def load_all_users():
        users = db.fetchall("users", ["user_id", "status"])
        return users


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
    exercise_name: str
    group_id: int
    english_name: str
    video: str


class Exercises:
    def __init__(self):
        self.test = 123

    def get_exercise_by_id(self, exercise_id: int):
        return self._get_filtered_data("exercise_id", exercise_id)

    def get_exercise_by_name(self, exercise_name: str):
        return self._get_filtered_data("exercise_name", exercise_name)

    def get_all_exercises_by_group(self, group_id: int):
        return self._get_filtered_data("group_id", group_id)

    @staticmethod
    def load_all_exercises():
        exercises = db.fetchall("exercises", ["exercise_id", "exercise_name"])
        return exercises

    def _get_filtered_data(self, filter_column: str, filter_value):
        self.all_exercises = db.filtered_select("exercises",
                                                ["exercise_id", "exercise_name", "group_id"],
                                                filter_column,
                                                filter_value)
        return self.all_exercises


class MusclesGroup:
    """Описание объекта Группа мышц"""
    group_id: int
    group_name: str
    href: str


class MusclesGroups:
    @staticmethod
    def load_groups():
        groups = db.fetchall("groups", ["group_id", "group_name"])
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
        # TODO реализация логики добавления подходов в БД
        # TODO реализация логики удаления подходов в БД

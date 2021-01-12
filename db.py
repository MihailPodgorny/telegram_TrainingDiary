import os

import sqlite3


conn = sqlite3.connect(os.path.join("db", "workout.db"))
cursor = conn.cursor()


def insert(table, column_values):
    pass


def fetchall(table, columns):
    pass


def delete(table, row_id):
    pass


def get_cursor():
    return cursor


def _init_db():
    """Initializing the database"""
    with open("create_db.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='workouts'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()

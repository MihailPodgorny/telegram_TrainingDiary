# import os
import sqlite3
from typing import Dict, List


# conn = sqlite3.connect(os.path.join("workout.db"))
conn = sqlite3.connect("workout.db")
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]):
    all_columns = ', '.join(columns)
    cursor.execute(f"SELECT {all_columns} FROM {table}")
    return _generate_result(columns)


def filtered_select(table: str, columns: List[str], filter_column: str, filter_value):
    all_columns = ', '.join(columns)
    cursor.execute(f"SELECT {all_columns} FROM {table} WHERE {filter_column} = {filter_value}")
    return _generate_result(columns)


def delete(table: str, row_id):
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE {table[:len(table)-1]}_id={row_id}")
    conn.commit()


def _generate_result(columns):
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_cursor():
    return cursor


def _init_db():
    """Initializing the database"""
    with open("create_db.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Check DB"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='workouts'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()

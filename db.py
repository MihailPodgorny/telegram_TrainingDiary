# import os
import sqlite3
from typing import Dict, List, Any

# TODO сделать logging вместо print
# TODO  сделать единую точку входа в модуль

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
    if isinstance(filter_value, str):
        filter_value = f"'{filter_value}'"
    print(f"SELECT {all_columns} FROM {table} WHERE {filter_column} = {filter_value}")
    cursor.execute(f"SELECT {all_columns} FROM {table} WHERE {filter_column} = {filter_value}")
    return _generate_result(columns)


def update_one(table: str, column: str, value, filter_column: str, filter_value):
    if isinstance(filter_value, str):
        filter_value = f"'{filter_value}'"
    cursor.execute(
        f"UPDATE {table} "
        f"SET {column} = {value} "
        f"WHERE {filter_column} = {filter_value}")
    conn.commit()


def update_all(table: str,  column_values: Dict, filter_column: str, filter_value):
    filter_value = _check_input_type(filter_value)
    _s = []
    [_s.append(f"{str(key)} = {_check_input_type(column_values[key])}") for key in column_values.keys()]
    values = ", ".join(_s)
    cursor.execute(
        f"UPDATE {table} "
        f"SET {values} "
        f"WHERE {filter_column} = {filter_value}")
    conn.commit()


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


def _check_input_type(value: Any):
    if isinstance(value, str):
        value = f"'{value}'"
    return value


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

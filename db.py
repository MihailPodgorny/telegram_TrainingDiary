from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import load_only


engine = create_engine('sqlite:///workouts.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


def create(model):
    session.add(model)
    session.commit()


def get_by_id(model, pk):
    item = session.query(model).get(pk)
    return item


def get_id_by_name(model, name):
    query = session.query(model).filter(model.name == name).first()
    return query.id


def get_user_id_by_chat(model, chat):
    query = session.query(model).filter(model.chat == chat).first()
    return query.id


def get_user_state_by_chat(model, chat):
    query = session.query(model).filter(model.chat == chat).first()
    return query.state


def get_user_load_by_chat(model, chat):
    query = session.query(model).filter(model.chat == chat).first()
    return query.load


def get_all_data(model, columns=None):
    if columns is None:
        query = session.query(model).all()
    else:
        query = session.query(model).options(load_only(*columns)).all()
    return query


def get_last_workout(model, user_id):
    query = session.query(model).filter(model.user_id == user_id).order_by(model.id.desc()).first()
    return query.id, query.date_now, query.start_time


def get_last_set(model, workout_id):
    query = session.query(model).filter(model.workout_id == workout_id).order_by(model.id.desc()).first()
    return query.id, query.workout_id, query.exercise_id, query.weight, query.reps


def delete(model, pk):
    item = session.query(model).get(pk)
    session.delete(item)
    session.commit()


def get_all_data_by_group_id(model, group_id):
    query = session.query(model).filter(model.group_id == group_id)
    return query


def update_user_state_and_load_by_chat_id(model, chat_id, state, load):
    session.query(model).filter(model.chat == chat_id).update({'state': state, 'load': load})
    session.commit()


def update_workout_by_id(model, workout_id, end_time, total_time):
    session.query(model).filter(model.id == workout_id).update(
        {'end_time': end_time, 'total_time': total_time})
    session.commit()


def get_count(model):
    rows = session.query(model.id).count()
    return rows

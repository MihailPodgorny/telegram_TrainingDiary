from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from db import Base, engine


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat = Column(Integer)
    state = Column(Integer, default=0)
    load = Column(Integer, default=0)

    workout = relationship("Workouts", back_populates="user",
                           cascade="all, delete", passive_deletes=True)


class Workouts(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    date_now = Column(Date, default=datetime.date(datetime.now()))
    start_time = Column(Time, default=datetime.time(datetime.now()))
    end_time = Column(Time, default=datetime.time(datetime.now()))
    total_time = Column(Integer, default=0)

    user = relationship("Users", back_populates="workout")
    set = relationship("Sets", back_populates="workout")


class MuscleGroups(Base):
    __tablename__ = 'muscle_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text_href = Column(String, default='', nullable=True)

    exercise = relationship("Exercises", back_populates="muscle_group")


class Exercises(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('muscle_groups.id', ondelete="SET NULL"))
    original_name = Column(String)
    similar_name = Column(String, default='', nullable=True)
    video_href = Column(String, default='', nullable=True)

    muscle_group = relationship("MuscleGroups", back_populates="exercise")
    set = relationship("Sets", back_populates="exercise")


class Sets(Base):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id', ondelete="CASCADE"))
    exercise_id = Column(Integer, ForeignKey('exercises.id', ondelete="SET NULL"))
    weight = Column(Integer)
    reps = Column(Integer)

    workout = relationship("Workouts", back_populates="set")
    exercise = relationship("Exercises", back_populates="set")


Base.metadata.create_all(engine)

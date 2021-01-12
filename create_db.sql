CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    telegram_id INTEGER
);

CREATE TABLE  workouts(
    workout_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date_now DATE,
    start_time TIME,
    end_time TIME,
    total_time INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE  sets(
    set_id INTEGER PRIMARY KEY,
    workout_id INTEGER,
    exercise_id INTEGER,
    weight INTEGER,
    reps INTEGER,
    FOREIGN KEY(workout_id) REFERENCES workouts(workout_id),
    FOREIGN KEY(exercise_id) REFERENCES exercises(exercise_id),
);

CREATE TABLE exercises(
    exercise_id INTEGER PRIMARY KEY,
    name INTEGER,
    group_id INTEGER,
    english_name VARCHAR(255),
    similar_name VARCHAR(255),
    video VARCHAR(255),
    FOREIGN KEY(group_id) REFERENCES groups(group_id),
);

CREATE TABLE groups(
    group_id INTEGER PRIMARY KEY,
    group_name INTEGER
);

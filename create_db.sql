CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    status INTEGER
);

CREATE TABLE  workouts (
    workout_id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER,
    date_ DATE,
    start_time TIME,
    end_time TIME,
    total_time INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE  sets (
    set_id VARCHAR(36) PRIMARY KEY,
    workout_id INTEGER,
    exercise_id INTEGER,
    weight INTEGER,
    reps INTEGER,
    FOREIGN KEY(workout_id) REFERENCES workouts(workout_id),
    FOREIGN KEY(exercise_id) REFERENCES exercises(exercise_id)
);

CREATE TABLE exercises (
    exercise_id INTEGER PRIMARY KEY,
    exercise_name VARCHAR(100),
    group_id INTEGER,
    english_name VARCHAR(100),
    similar_name VARCHAR(100),
    video VARCHAR(255),
    FOREIGN KEY(group_id) REFERENCES groups(group_id)
);

CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY,
    group_name INTEGER,
    href VARCHAR(255)
);

INSERT INTO groups (group_id, group_name, href)
VALUES
    (1, "грудные", "http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%B3%D1%80%D1%83%D0%B4%D0%B8"),
    (2, "спина", "http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D1%81%D0%BF%D0%B8%D0%BD%D1%8B"),
    (3, "ноги", "http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%BD%D0%BE%D0%B3"),
    (4, "плечи", "http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D0%BF%D0%BB%D0%B5%D1%87%D0%B5%D0%B2%D0%BE%D0%B3%D0%BE_%D0%BF%D0%BE%D1%8F%D1%81%D0%B0"),
    (5, "руки", "http://sportwiki.to/%D0%9C%D1%8B%D1%88%D1%86%D1%8B_%D1%80%D1%83%D0%BA"),
    (6, "прочее", "http://sportwiki.to/%D0%AD%D0%BD%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F_%D0%B1%D0%BE%D0%B4%D0%B8%D0%B1%D0%B8%D0%BB%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0");

INSERT INTO exercises (exercise_id, exercise_name, group_id, english_name, similar_name, video)
VALUES
    (1, "жим_лежа", 1, "Bench press", "123", "123"),
    (2, "становая_тяга", 6, "Deadlifts", "33", "33"),
    (3, "приседания", 3, "41", "14", "134"),
    (4, "жим_гантелей_30", 1, "Bench press 30", "123", "123");
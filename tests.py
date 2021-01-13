import db
from workouts import User, Users

# check insert
table = "users"
column_values = {
    "user_id": 123,
    "telegram_id": "qwert"
}
db.insert(table, column_values)

# check delete
id = 123
db.delete(table, id)

# Check class Users

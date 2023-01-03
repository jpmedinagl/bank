from utils.database_connection import DatabaseConnection
from utils.user import User
from typing import List

user_database = 'users.db'
data_database = 'data.db'


def create_bank_tables() -> None:
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'username TEXT NOT NULL, '
                       'password TEXT NOT NULL'
                       ')')

    with DatabaseConnection(data_database) as connection:
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS balances(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'checking, savings, investments)')


def log_user(user: User) -> List:
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (user.username, user.password))
        user_info = cursor.fetchall()

    return user_info


def create_user(user: User):
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO users (id, username, password) VALUES(NULL, ?, ?)", (user.username, user.password))


def get_all_users():
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users')
        users = [
            {'id': row[0], 'user': User(username=row[1], password=row[2])} for row in cursor.fetchall()
        ]

    return users

from utils.database_connection import DatabaseConnection
from utils.user import User
from typing import List
import os

database = os.path.dirname(os.path.abspath('app.py')) + '/databases'
user_database = database + '/users.db'
data_database = database + '/data.db'


def create_bank_tables() -> None:
    try:
        os.makedirs(database)
    except FileExistsError:
        pass

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

    with DatabaseConnection(data_database) as connection:
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO users (id, checking, savings, investments) VALUES (NULL, 0, 0, 0)")


def get_all_users():
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users')
        users = [
            {'id': row[0], 'user': User(username=row[1], password=row[2])} for row in cursor.fetchall()
        ]

    return users


def delete_user(username: str) -> None:
    with DatabaseConnection(user_database) as connection:
        cursor = connection.cursor()

        cursor.execute('DELETE FROM users WHERE username=?', (username,))


def add_money(user: User, account: str, amount: str) -> None:
    # need to get the user row
    with DatabaseConnection(data_database) as connection:
        cursor = connection.cursor()

        cursor.execute(f'UPDATE data set ', (account, amount))

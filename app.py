from utils import database
from utils.user import User

MENU_1 = """
Welcome to JP Bank!
Enter:
- 'e' if you are an existing user
- 'c' to create an account with us
- 'q' to quit

Your choice: """

MENU_2 = """
Enter:
- 'a' to add money to your account
- 'l' to list all of your balances
- 'q' to log out of your account

Your choice: """


def menu_1():
    database.create_bank_tables()
    user_input_1 = input(MENU_1)
    while user_input_1 != 'q':
        if user_input_1 in selection_1:
            selected_function = selection_1[user_input_1]
            user = selected_function()
            if user:
                menu_2()
        else:
            print(f"Unknown command '{user_input_1}'. Please try again.")

        user_input_1 = input(MENU_1)


def menu_2():

    user_input_2 = input(MENU_2)
    while user_input_2 != 'q':
        if user_input_2 in selection_2:
            selected_function = selection_2[user_input_2]
            selected_function()
        else:
            print(f"Unknown command '{user_input_2}'. Please try again.")


def prompt_existing_user():
    attempt = 1
    while True and attempt <= 3:
        username = input('Enter your username: ')
        password = input('Enter your password: ')

        user = User(username, password)
        if database.log_user(user):
            print(f"Log in complete! Welcome {user.username}.")
            return user
        attempt += attempt
        print(f"Incorrect username and/or password.")
    else:
        print(f"Log in failed! Please try again.")


def create_user_account():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    user = User(username, password)
    database.create_user(user)
    print(f'User {user.username} created!')


def list_all_users():
    users = database.get_all_users()
    for user in users:
        print(f"{user['id']}. username: {user['user'].username}, password: {user['user'].password}")


def user_add_to_account():
    pass


def user_list_balance():
    pass


def prompt_delete_user():
    username = input('Enter username you would like to delete: ')

    user_in = _user_in_database(username)

    if user_in:
        database.delete_user(username)
        print(f"{username} was deleted.")
    else:
        print(f"{username} not in database")


def _user_in_database(username):
    users = database.get_all_users()

    for user in users:
        if username in user['user'].username:
            return True
    else:
        return False


selection_1 = {
    'e': prompt_existing_user,
    'c': create_user_account,
    'l': list_all_users,
    'd': prompt_delete_user
}

selection_2 = {
    'a': user_add_to_account,
    'l': user_list_balance,
}

menu_1()

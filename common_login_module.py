import getpass
import colorama
from termcolor import colored

colorama.init()

def login(database, CURSOR) -> tuple[str, str, str]:  # returns (username, mentor_name, password). None in both if login fails.

    print(colored("Enter UserID : ", 'cyan'))
    user_name = input(colored(">> ", 'green'))

    if len(user_name) == 0:
        print(colored("User name cannot be empty", 'red'))
        return None, None, None

    print(colored("Enter Password : ", 'cyan'))
    pass_key = getpass.getpass(colored(">> ", 'green'))
    print()

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print(colored(f"UserID {user_name} doesn't exist. Please Sign Up", 'red'))
        print()
        print()
    else:
        data = CURSOR.fetchone()
        if pass_key != data[1]:
            print(colored("Invalid Password", 'red'))
            print()
            print()
        else:
            print(colored("Login Successful", 'green'))
            print(colored(f"Welcome {user_name}", 'light_magenta'))
            print()
            print()
            if len(data) == 3: # if mentor in data
                mentor_name = data[2]
                return user_name, mentor_name, pass_key
            return user_name, None, pass_key

    return None, None, None

def sign_up(database, CURSOR, connect, mentor_name=None): # returns (USERNAME, MENTOR_NAME, pass) on success

    print(colored("Enter UserID : ", 'cyan'))
    user_name = input(colored(">> ", 'green'))
    if len(user_name) == 0:
        print(colored("Please enter a valid username", 'red'))
        return False
    
    print(colored("Enter Password : ", 'cyan'))
    pass_key = input(colored(">> ", 'green'))
    if len(pass_key) < 4:
        print(colored("Password must be at least 4 characters", 'red'))
        print()
        print()
        return False

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print(colored("Registration Successful.", 'green'))
        if mentor_name:
            CURSOR.execute(f'INSERT INTO {database}(USER_NAME, PASSWD, MENTOR_NAME) VALUES("{user_name}", "{pass_key}", "{mentor_name}")')
        else:
            CURSOR.execute(f'INSERT INTO {database}(USER_NAME, PASSWD) VALUES("{user_name}", "{pass_key}")')
        connect.commit()
        print()
        print()
        return (user_name, mentor_name, pass_key)
    else:
        print(colored(f"User ID {user_name} already exists.", 'red'))
        print()
        print()
        return False
    
def update_passkey(database, user_name, CURSOR, connect) -> str: # returns password, as that's what has changed
    print(colored("Enter Old Password : ", 'cyan'))
    pass_key = getpass.getpass(colored(">> ", 'green'))
    print()

    CURSOR.execute(f'SELECT * FROM {database} WHERE USER_NAME="{user_name}"')

    if CURSOR.rowcount == 0:
        print(colored(f"UserID {user_name} doesn't exist. Please Sign Up", 'red'))
        print()
        print()
        return pass_key
    else:
        data = CURSOR.fetchone()
        if pass_key != data[1]:
            print(colored("Invalid Password", 'red'))
            print()
            print()
            return pass_key
        else:
            print(colored("Enter new Password : ", 'cyan'))
            pass_key = input(colored(">> ", 'green'))
            
            print("Password Changed Successfully!")
            print()
            print()

            CURSOR.execute(f'UPDATE {database} SET PASSWD = "{pass_key}" WHERE USER_NAME = "{user_name}"')
            connect.commit()
            
            return pass_key

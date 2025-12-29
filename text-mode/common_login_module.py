import getpass
import colorama
from termcolor import colored
import re
from typing import Optional, Tuple
from config import StudensTableConfig, TeachersTableConfig

colorama.init()

def sanitize_input(input_str: str) -> Optional[str]:
    """Sanitize user input to prevent SQL injection and other security issues."""
    if not input_str:
        return None
    
    # Remove any SQL injection attempts
    input_str = re.sub(r'[\'";]', '', input_str)
    
    # Remove any potential command injection characters
    input_str = re.sub(r'[&|;`$]', '', input_str)
    
    # Remove any whitespace from beginning and end
    input_str = input_str.strip()
    
    # Replace multiple spaces with a single space
    input_str = re.sub(r'\s+', ' ', input_str)
    
    return input_str if input_str else None

def validate_username(username: str) -> bool:
    """Validate username format.
    Allows letters, numbers, spaces, underscores, and hyphens.
    Spaces are allowed but not at the start or end.
    """
    if not username:
        return False
    
    # Username should be alphanumeric with spaces, underscores and hyphens
    # Spaces allowed but not at start/end, and not multiple spaces in a row
    return bool(re.match(r'^[a-zA-Z0-9_-]+(?: [a-zA-Z0-9_-]+)*$', username)) and 3 <= len(username) <= 50

def validate_password(password: str) -> bool:
    """Validate password strength.
    Only requires a minimum length of 4 characters.
    """
    if not password:
        return False
    
    # Password should be at least 4 characters
    return len(password) >= 4

def login(database: str, CURSOR) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Login function with input sanitization."""
    print(colored("Enter UserID : ", 'cyan'))
    user_name = sanitize_input(input(colored(">> ", 'green')))

    if not user_name or not validate_username(user_name):
        print(colored("Invalid username format. Use only letters, numbers, underscores, and hyphens (3-50 characters).", 'red'))
        return None, None, None

    mentor_name = None

    if database == StudensTableConfig.STUDENTS_TABLE:
        print(colored("Select the Mentor to be logged in for : ", 'cyan'))

        CURSOR.execute(f'SELECT DISTINCT {StudensTableConfig.MENTOR_NAME} FROM {StudensTableConfig.STUDENTS_TABLE} WHERE {StudensTableConfig.USER_NAME} = %s', (user_name,))

        if CURSOR.rowcount == 0:
            print(colored(f"UserID {user_name} doesn't exist. Please Sign Up", 'red'))
            print()
            print()
            return None, None, None
        mentors = [row[0] for row in CURSOR.fetchall()]

        for i, mentor in enumerate(mentors, 1):
            print(f"{i}. {mentor}")
        
        mentor_choice = input(colored(">> ", 'green'))
        if not mentor_choice.isdigit() or not (1 <= int(mentor_choice) <= len(mentors)):
            print(colored("Invalid choice for mentor.", 'red'))
            return None, None, None
        
        mentor_name = mentors[int(mentor_choice) - 1]
        
        if not mentor_name or not validate_username(mentor_name):
            print(colored("Invalid mentor name format.", 'red'))
            return None, None, None

    try:
        if mentor_name:
            CURSOR.execute(f'SELECT {StudensTableConfig.USER_NAME}, {StudensTableConfig.PASSWORD}, {StudensTableConfig.MENTOR_NAME} FROM {database} WHERE {StudensTableConfig.USER_NAME} = %s AND {StudensTableConfig.MENTOR_NAME} = %s', (user_name, mentor_name))
        else:
            CURSOR.execute(f'SELECT {TeachersTableConfig.USER_NAME}, {TeachersTableConfig.PASSWORD} FROM {database} WHERE {TeachersTableConfig.USER_NAME} = %s', (user_name,))

        if CURSOR.rowcount == 0:
            if database == StudensTableConfig.STUDENTS_TABLE:
                print(colored(f"UserID {user_name} with Mentor {mentor_name} doesn't exist. Please Sign Up", 'red'))
            else:
                print(colored(f"UserID {user_name} doesn't exist. Please Sign Up", 'red'))
            print()
            print()
        else:
            print(colored("Enter Password : ", 'cyan'))
            pass_key = getpass.getpass(colored(">> ", 'green'))
            print()

            if not pass_key:
                print(colored("Password cannot be empty", 'red'))
                return None, None, None

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
                if database == StudensTableConfig.STUDENTS_TABLE:
                    mentor_name = data[2]
                    return user_name, mentor_name, pass_key
                return user_name, None, pass_key
    except Exception as e:
        print(colored(f"An error occurred during login: {str(e)}", 'red'))
        return None, None, None

    return None, None, None

def sign_up(database: str, CURSOR, connect, mentor_name: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Sign up function with input sanitization."""
    print(colored("Enter UserID : ", 'cyan'))
    user_name = sanitize_input(input(colored(">> ", 'green')))
    
    if not user_name or not validate_username(user_name):
        print(colored("Invalid username format. Use only letters, numbers, underscores, and hyphens (3-50 characters).", 'red'))
        return False
    
    print(colored("Enter Password : ", 'cyan'))
    pass_key = getpass.getpass(colored(">> ", 'green'))
    
    if not validate_password(pass_key):
        print(colored("Password must be at least 4 characters and contain both letters and numbers.", 'red'))
        print()
        print()
        return False

    try:
        if mentor_name:
            CURSOR.execute(f'SELECT * FROM {StudensTableConfig.STUDENTS_TABLE} WHERE {StudensTableConfig.USER_NAME} = %s AND {StudensTableConfig.MENTOR_NAME} = %s', (user_name, mentor_name))
        else:
            CURSOR.execute(f'SELECT * FROM {TeachersTableConfig.TEACHERS_TABLE} WHERE {TeachersTableConfig.USER_NAME} = %s', (user_name,))

        if CURSOR.rowcount == 0:
            print(colored("Registration Successful.", 'green'))
            try:
                if mentor_name:
                    CURSOR.execute(f'INSERT INTO {database}({StudensTableConfig.USER_NAME}, {StudensTableConfig.PASSWORD}, {StudensTableConfig.MENTOR_NAME}) VALUES(%s, %s, %s)', 
                                 (user_name, pass_key, mentor_name))
                else:
                    CURSOR.execute(f'INSERT INTO {database}({TeachersTableConfig.USER_NAME}, {TeachersTableConfig.PASSWORD}) VALUES(%s, %s)', 
                                 (user_name, pass_key))
                connect.commit()
                print()
                print()
                return (user_name, mentor_name, pass_key)
            except Exception as e:
                print(colored(f"Error during registration: {str(e)}", 'red'))
                connect.rollback()
                return False
        else:
            print(colored(f"User ID {user_name} already exists.", 'red'))
            print()
            print()
            return False
    except Exception as e:
        print(colored(f"An error occurred during sign up: {str(e)}", 'red'))
        return False

def update_passkey(database: str, user_name: str, CURSOR, connect, mentor_name: Optional[str] = None) -> str:
    """Update password function with input sanitization."""
    if not validate_username(user_name):
        print(colored("Invalid username format", 'red'))
        return ""

    print(colored("Enter Old Password : ", 'cyan'))
    pass_key = getpass.getpass(colored(">> ", 'green'))
    print()

    if not pass_key:
        print(colored("Password cannot be empty", 'red'))
        return ""

    try:
        if not mentor_name:
            CURSOR.execute(f'SELECT * FROM {database} WHERE {TeachersTableConfig.USER_NAME} = %s', (user_name,))
        else:
            CURSOR.execute(f'SELECT * FROM {database} WHERE {StudensTableConfig.USER_NAME} = %s AND {StudensTableConfig.MENTOR_NAME} = %s', (user_name, mentor_name))

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
                new_pass_key = getpass.getpass(colored(">> ", 'green'))
                
                if not validate_password(new_pass_key):
                    print(colored("Password must be at least 4 characters and contain both letters and numbers.", 'red'))
                    print()
                    print()
                    return pass_key
                
                try:
                    if not mentor_name:
                        CURSOR.execute(f'UPDATE {database} SET {TeachersTableConfig.PASSWORD} = %s WHERE {TeachersTableConfig.USER_NAME} = %s', 
                                     (new_pass_key, user_name))
                    else:
                        CURSOR.execute(f'UPDATE {database} SET {StudensTableConfig.PASSWORD} = %s WHERE {StudensTableConfig.USER_NAME} = %s AND {StudensTableConfig.MENTOR_NAME} = %s', 
                                     (new_pass_key, user_name, mentor_name))
                    connect.commit()
                    
                    print(colored("Password Changed Successfully!", 'green'))
                    print()
                    print()
                    return new_pass_key
                except Exception as e:
                    print(colored(f"Error updating password: {str(e)}", 'red'))
                    connect.rollback()
                    return pass_key
    except Exception as e:
        print(colored(f"An error occurred during password update: {str(e)}", 'red'))
        return pass_key

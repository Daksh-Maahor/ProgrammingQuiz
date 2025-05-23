from init_sql import get_db_connection, close_db_connection
import teachers_module
import students_module
import colorama
from termcolor import colored

colorama.init()

IS_TEACHER = 1
IS_STUDENT = 2
QUIT = 3

def main():
    running = True
    connection, cursor = get_db_connection()

    while running:
        print(colored("     Programming Quiz    ", 'green'))

        print(colored("Select an Option (1 or 2)", 'cyan'))
        print("1. Teacher")
        print("2. Student")
        print("3. Quit")

        choice = input(colored(">> ", 'green'))

        if choice.isnumeric():
            choice = int(choice)

            if choice == IS_TEACHER:
                teachers_module.main(cursor, connection)
            elif choice == IS_STUDENT:
                students_module.main(cursor, connection)
            elif choice == QUIT:
                running = False
            else:
                print(colored("Not a valid option", 'red'))
            
        else:
            print(colored("Not a valid option", 'red'))

if __name__ == "__main__":
    main()
    close_db_connection()

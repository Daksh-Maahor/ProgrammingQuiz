from init_sql import CURSOR, connect, close
import teachers_module
import students_module

IS_TEACHER = 1
IS_STUDENT = 2
QUIT = 3

def main():
    running = True

    while running:
        print("Select an Option (1 or 2)")
        print("1. Teacher")
        print("2. Student")
        print("3. Quit")

        choice = input(">> ")

        if choice.isnumeric():
            choice = int(choice)

            if choice == IS_TEACHER:
                teachers_module.main(CURSOR, connect)
            elif choice == IS_STUDENT:
                students_module.main(CURSOR, connect)
            elif choice == QUIT:
                running = False
            else:
                print("Not a valid option")
            
        else:
            print("Not a valid option")

if __name__ == "__main__":
    main()
    close()

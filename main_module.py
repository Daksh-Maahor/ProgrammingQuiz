import __init__
import teachers_module
import students_module

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

            if choice == 1:
                teachers_module.main()
            elif choice == 2:
                students_module.main()
            elif choice == 3:
                running = False
            else:
                print("Not a valid option")
            
        else:
            print("Not a valid option")

if __name__ == "__main__":
    main()

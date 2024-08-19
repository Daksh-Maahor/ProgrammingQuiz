import json
import mysql
import mysql.connector
import __init__

def login():
    pass

def sign_up():
    pass

def main():
    print("----   Programming Quiz   ----")
    print("----   Teacher's Module   ----")

    print()

    print("Select An Option")
    print("1. Login")
    print("2. Sign Up")

    choice = input(">> ")

    if choice == 1:
        login()
    elif choice == 2:
        sign_up()
    else:
        print("Invalid Choice")
        return

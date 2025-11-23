import colorama
from termcolor import colored
import getpass
from prettytable import PrettyTable
from config import StudensTableConfig, TeachersTableConfig, QuestionsTableConfig, QuizAttemptsTableConfig

colorama.init()

CDM_CHOICE_DATA_CLEAR          = 1
CDM_CHOICE_SELECTED_DATA_CLEAR = 2

def pretty_print(dictionary, indent=0, index=False):
    for k, i in enumerate(dictionary):
        if index:
            print()
            print()
            print("    " * indent, f"{k}:")
        print("    "*indent + str(i), ":")
        j = dictionary[i]
        if type(j) == dict:
            pretty_print(j, indent+1)
        elif type(j) == list:
            pretty_print_list(j, indent=indent+1)
        else:
            print("    "*(indent+1) + str(j))

def pretty_print_list(lst, title='', indent=0, index=False):
    print('    '*(indent), title, ":\n")
    for j, i in enumerate(lst):
        if index:
            print()
            print()
            print("    " * indent, f"{j}:")

        if type(i) == list:
            pretty_print_list(i, indent=indent+1)
        elif type(i) == dict:
            pretty_print(i, indent+1)
        else:
            print('   '*(indent+1), i)

def delete_account(user_name, CURSOR, connect, database):
    try:
        if database == TeachersTableConfig.TEACHERS_TABLE:
            CURSOR.execute(f'DELETE FROM {QuestionsTableConfig.QUESTIONS_TABLE} WHERE {QuestionsTableConfig.MENTOR_ID} = %s', (user_name,))
            connect.commit()
            CURSOR.execute(f'DELETE FROM {StudensTableConfig.STUDENTS_TABLE} WHERE {StudensTableConfig.MENTOR_NAME} = %s', (user_name,))
            connect.commit()
            CURSOR.execute(f'DELETE FROM {database} WHERE {TeachersTableConfig.USER_NAME} = %s', (user_name,))
            connect.commit()
        else:
            CURSOR.execute(f'DELETE FROM {QuizAttemptsTableConfig.QUIZ_ATTEMPTS_TABLE} WHERE {QuizAttemptsTableConfig.STUDENT_NAME} = %s', (user_name,))
            connect.commit()
            CURSOR.execute(f'DELETE FROM {database} WHERE {TeachersTableConfig.USER_NAME} = %s', (user_name,))
            connect.commit()
        
        print(colored(f"Account '{user_name}' deleted successfully.", 'green'))
    except Exception as e:
        print(colored(f"Error deleting account: {str(e)}", 'red'))

def delete_questions(user_name, passwd, CURSOR, connect):
    print(colored("Select : ", 'cyan'))
    print("1. Clear All Questions")
    print("2. Clear Selected Questions")

    choice = input(colored(">> ", 'green'))
    passs = getpass.getpass(colored("Enter password to continue : ", 'red'))

    if passs == passwd:
        if not choice.isnumeric():
            print(colored("Invalid Choice", 'red'))
        else:
            choice = int(choice)

            if choice == 1:
                try:
                    CURSOR.execute(f'DELETE FROM {QuestionsTableConfig.QUESTIONS_TABLE} WHERE {QuestionsTableConfig.MENTOR_ID} = %s', (user_name,))
                    connect.commit()
                    print(colored("All questions cleared.", 'green'))
                except Exception as e:
                    print(colored(f"Error clearing questions: {str(e)}", 'red'))

            elif choice == 2:
                try:
                    CURSOR.execute(f'SELECT {QuestionsTableConfig.ID}, {QuestionsTableConfig.QUESTION_TEXT}, {QuestionsTableConfig.OPTIONS}, {QuestionsTableConfig.DIFFICULTY}, {QuestionsTableConfig.CONCEPTS} FROM {QuestionsTableConfig.QUESTIONS_TABLE} WHERE {QuestionsTableConfig.MENTOR_ID} = %s', (user_name,))
                    questions = CURSOR.fetchall()

                    if not questions:
                        print(colored("No questions found.", 'yellow'))
                        return

                    qns_table = PrettyTable(["Q. No.", "Question", "Options", "Difficulty", "Concepts"])
                    for idx, qn in enumerate(questions):
                        qns_table.add_row([idx+1, qn[1][:50], qn[2][:50], qn[3], qn[4][:50]])
                        qns_table.add_row(["", "", "", "", ""])
                    
                    print(qns_table)
                    print()

                    print(colored("Select an index to remove : ", 'cyan'))
                    idx = input(colored(">> ", 'green'))

                    if not idx.isnumeric():
                        print("Invalid Input")
                    else:
                        idx = int(idx) - 1
                        if 0 <= idx < len(questions):
                            question_id = questions[idx][0]
                            CURSOR.execute(f'DELETE FROM {QuestionsTableConfig.QUESTIONS_TABLE} WHERE {QuestionsTableConfig.ID} = %s', (question_id,))
                            connect.commit()
                            print(colored("Question deleted.", 'green'))
                        else:
                            print(colored("Invalid index", 'red'))
                except Exception as e:
                    print(colored(f"Error: {str(e)}", 'red'))
    else:
        print(colored("Incorrect password.", 'red'))


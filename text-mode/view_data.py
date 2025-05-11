import pickle
import clear_data_module
from prettytable import PrettyTable
import init_sql
import colorama
from termcolor import colored
import json
from init_sql import DatabaseConfig, get_db_connection
from datetime import datetime, timedelta

colorama.init()

STUDENTS_DATABASE = "students_login_data"
TEACHERS_DATABASE = "teachers_login_data"

VM_CHOICE_DATA_VIEW = 1
VM_CHOICE_DATA_CLEAR = 2
VM_CHOICE_SELECTED_DATA_CLEAR = 3

# to print the data in dictionaries
def pretty_print(dictionary, indent=0):
    for i in dictionary:
        print("    "*indent + str(i), ":")
        j = dictionary[i]
        if type(j) == dict:
            pretty_print(j, indent+1)
        elif type(j) == list:
            pretty_print_list(j, indent=indent+1)
        else:
            print("    "*(indent+1) + str(j))
            
# to print data in lists
def pretty_print_list(lst, title='', indent=0):
    print('    '*(indent), title, ":\n")
    for i in lst:
        if type(i) == list:
            pretty_print_list(i, indent=indent+1)
        elif type(i) == dict:
            pretty_print(i, indent+1)
        else:
            print('   '*(indent+1), i)

def delete_account(user_name, CURSOR, connect, database):
    clear_data_module.delete_account(user_name, CURSOR, connect, database)

def view_students(user_name, CURSOR):
    """View all students of a teacher in a nicely formatted list."""
    CURSOR.execute(f'SELECT USER_NAME FROM {STUDENTS_DATABASE} WHERE MENTOR_NAME = %s', (user_name,))
    students = CURSOR.fetchall()
    
    if not students:
        print(colored(f"\nNo students found for {user_name}", 'yellow'))
        print()
        return
    
    # Print header
    print("\n" + "=" * 50)
    print(colored(f"Students of {user_name}", 'green').center(50))
    print("=" * 50)
    
    # Print student names with bullet points
    for i, student in enumerate(students, 1):
        print(colored(f"• {student[0]}", 'cyan'))
    
    # Print footer
    print("=" * 50)
    print(colored(f"Total Students: {len(students)}", 'yellow').center(50))
    print("=" * 50 + "\n")

def view_students_performance(user_name):
    """View performance statistics of students in a nicely formatted way."""
    connection, cursor = get_db_connection()
    
    # Get all students for this teacher
    cursor.execute(f'SELECT USER_NAME FROM {STUDENTS_DATABASE} WHERE MENTOR_NAME = %s', (user_name,))
    students = cursor.fetchall()
    
    if not students:
        print(colored(f"\nNo students found for {user_name}", 'yellow'))
        print()
        return
    
    # Print header
    print("\n" + "=" * 50)
    print(colored(f"Students of {user_name}", 'green').center(50))
    print("=" * 50)
    
    # Print student list with numbers
    for i, student in enumerate(students, 1):
        print(colored(f"{i}. {student[0]}", 'cyan'))
    
    print("=" * 50)
    print(colored(f"Total Students: {len(students)}", 'yellow').center(50))
    print("=" * 50 + "\n")
    
    # Get teacher's choice
    while True:
        try:
            choice = int(input(colored("Enter student number to view performance (0 to exit): ", 'green')))
            if choice == 0:
                return
            if 1 <= choice <= len(students):
                break
            print(colored("Invalid choice. Please try again.", 'red'))
        except ValueError:
            print(colored("Please enter a valid number.", 'red'))
    
    selected_student = students[choice - 1][0]
    
    # Get all attempts for this student
    query = f"""
        SELECT 
            a.quiz_session_id,
            MIN(a.attempt_date) as attempt_start,
            COUNT(*) as total_questions,
            SUM(CASE WHEN a.selected_answer = q.correct_answer THEN 1 ELSE 0 END) as correct_answers
        FROM quiz_attempts a
        JOIN {DatabaseConfig.QUESTIONS_TABLE} q ON a.question_id = q.id
        WHERE a.student_name = %s AND q.teacher_id = %s
        GROUP BY a.quiz_session_id
        ORDER BY attempt_start DESC
    """
    params = (selected_student, user_name)
    cursor.execute(query, params)
    
    attempts = cursor.fetchall()
    
    if not attempts:
        print(colored("No quiz attempts found for this student.", 'yellow').center(80))
        print("=" * 80 + "\n")
        return

    # Print attempts list
    print("\n" + "=" * 80)
    print(colored(f"Quiz Attempts for {selected_student}", 'green').center(80))
    print("=" * 80)
    
    # Create a table for attempts
    table = PrettyTable(["No.", "Date & Time", "Questions", "Score"])
    for i, attempt in enumerate(attempts, 1):
        session_id, attempt_start, total_questions, correct_answers = attempt
        date_str = attempt_start.strftime('%Y-%m-%d %H:%M:%S')
        # Ensure we're using numeric values for the calculation
        total_questions = int(total_questions)
        correct_answers = int(correct_answers)
        score_percent = int((correct_answers/total_questions)*100) if total_questions > 0 else 0
        table.add_row([
            i,
            date_str,
            f"{correct_answers}/{total_questions}",
            f"{score_percent}%"
        ])
    
    print(table)
    print("=" * 80)
    
    # Get teacher's choice of attempt
    while True:
        try:
            attempt_choice = int(input(colored("Enter attempt number to analyze (0 to exit): ", 'green')))
            if attempt_choice == 0:
                return
            if 1 <= attempt_choice <= len(attempts):
                break
            print(colored("Invalid choice. Please try again.", 'red'))
        except ValueError:
            print(colored("Please enter a valid number.", 'red'))
    
    selected_session = attempts[attempt_choice - 1][0]
    
    # Get detailed questions for the selected attempt
    cursor.execute(f"""
        SELECT 
            q.question_text,
            q.concepts,
            q.correct_answer,
            a.selected_answer,
            a.time_taken,
            q.difficulty
        FROM quiz_attempts a
        JOIN {DatabaseConfig.QUESTIONS_TABLE} q ON a.question_id = q.id
        WHERE a.student_name = %s 
        AND q.teacher_id = %s 
        AND a.quiz_session_id = %s
        ORDER BY a.attempt_date
    """, (selected_student, user_name, selected_session))
    
    questions = cursor.fetchall()
    
    if not questions:
        print(colored("No questions found for this attempt.", 'yellow').center(80))
        print("=" * 80 + "\n")
        return

    # Print header for performance report
    print("\n" + "=" * 80)
    print(colored(f"Performance Report for {selected_student}", 'green').center(80))
    print(colored(f"Date & Time: {attempts[attempt_choice - 1][1].strftime('%Y-%m-%d %H:%M:%S')}", 'yellow').center(80))
    print("=" * 80)
    
    # Print Overall Analysis
    print("\n" + "=" * 80)
    print(colored("Overall Performance Analysis", 'green').center(80))
    print("=" * 80)
    
    # Calculate difficulty-wise analysis
    difficulty_stats = {'EASY': {'correct': 0, 'incorrect': 0, 'total': 0},
                       'MEDIUM': {'correct': 0, 'incorrect': 0, 'total': 0},
                       'HARD': {'correct': 0, 'incorrect': 0, 'total': 0}}
    
    # Calculate concept-wise analysis
    concept_stats = {}
    total_correct = 0
    
    for question in questions:
        question_text, concepts_json, correct_answer, selected_answer, time_taken, difficulty = question
        concepts = json.loads(concepts_json)
        is_correct = selected_answer == correct_answer
        
        # Update difficulty stats
        difficulty_stats[difficulty]['total'] += 1
        if is_correct:
            difficulty_stats[difficulty]['correct'] += 1
            total_correct += 1
        else:
            difficulty_stats[difficulty]['incorrect'] += 1
        
        # Update concept stats
        for concept in concepts:
            if concept not in concept_stats:
                concept_stats[concept] = {'correct': 0, 'incorrect': 0, 'total': 0}
            concept_stats[concept]['total'] += 1
            if is_correct:
                concept_stats[concept]['correct'] += 1
            else:
                concept_stats[concept]['incorrect'] += 1
    
    # Print total score
    print("\n" + colored("Total Score", 'cyan').center(80))
    print("-" * 80)
    print(colored(f"Correct: {total_correct}", 'green').center(40) + 
          colored(f"Incorrect: {len(questions) - total_correct}", 'red').center(40))
    print(colored(f"Total Questions: {len(questions)}", 'yellow').center(40) + 
          colored(f"Score: {int(total_correct/len(questions)*100)}%", 'yellow').center(40))
    
    # Print difficulty-wise analysis
    print("\n" + colored("Performance by Difficulty Level", 'cyan').center(80))
    print("-" * 80)
    for difficulty in ['EASY', 'MEDIUM', 'HARD']:
        stats = difficulty_stats[difficulty]
        if stats['total'] > 0:
            correct = int(stats['correct'])
            total = int(stats['total'])
            score = int((correct/total)*100) if total > 0 else 0
            print(colored(f"{difficulty}", 'yellow').center(20) + 
                  colored(f"Correct: {correct}", 'green').center(20) + 
                  colored(f"Incorrect: {stats['incorrect']}", 'red').center(20) + 
                  colored(f"Score: {score}%", 'yellow').center(20))
    
    # Print concept-wise analysis
    print("\n" + colored("Performance by Concept", 'cyan').center(80))
    print("=" * 80)
    
    # Create a table-like structure for concepts
    concept_width = 25
    stats_width = 15
    
    # Print header
    print(colored("Concept".ljust(concept_width), 'yellow') + 
          colored("Correct".center(stats_width), 'green') + 
          colored("Incorrect".center(stats_width), 'red') + 
          colored("Score".center(stats_width), 'yellow'))
    print("-" * 80)
    
    # Sort concepts by score percentage for better visualization
    sorted_concepts = sorted(
        [(concept, stats) for concept, stats in concept_stats.items() 
         if concept not in ['EASY', 'MEDIUM', 'HARD']],
        key=lambda x: x[1]['correct'] / x[1]['total'] if x[1]['total'] > 0 else 0,
        reverse=True
    )
    
    for concept, stats in sorted_concepts:
        correct = int(stats['correct'])
        total = int(stats['total'])
        score_percent = int((correct/total)*100) if total > 0 else 0
        # Color the score based on performance
        score_color = 'green' if score_percent >= 70 else 'yellow' if score_percent >= 50 else 'red'
        
        print(colored(concept[:concept_width].ljust(concept_width), 'cyan') + 
              colored(str(correct).center(stats_width), 'green') + 
              colored(str(stats['incorrect']).center(stats_width), 'red') + 
              colored(f"{score_percent}%".center(stats_width), score_color))
    
    print("=" * 80)
    
    # Print question-wise analysis
    print("\n" + "=" * 80)
    print(colored("Question-wise Analysis", 'green').center(80))
    print("=" * 80)
    
    for i, question in enumerate(questions, 1):
        question_text, concepts_json, correct_answer, selected_answer, time_taken, difficulty = question
        concepts = json.loads(concepts_json)
        
        print("\n" + "-" * 80)
        print(colored(f"Question {i}:", 'green'))
        print(question_text)
        print()
        
        print(colored("Concepts:", 'blue'))
        print(", ".join(concepts))
        print()

        print(colored("Time Taken:", 'yellow'))
        print(f"{time_taken:.2f} seconds")
        print()

        is_correct = selected_answer == correct_answer
        print(colored("Result:", 'green' if is_correct else 'red'))
        print("Correct" if is_correct else "Incorrect")
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print(colored("End of Report", 'green').center(80))
    print("=" * 80 + "\n")

def view_quiz(teacher_id):
    connection, cursor = get_db_connection()
    
    # Get all unique concepts for this teacher
    cursor.execute(f"SELECT DISTINCT concepts FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE teacher_id = %s", (teacher_id,))
    concepts_list = []
    for row in cursor.fetchall():
        if row[0]:  # if concepts is not None
            concepts = json.loads(row[0])
            concepts_list.extend(concepts)
    concepts_list = list(set(concepts_list))  # remove duplicates
    
    # Separate concepts by type (difficulty levels and actual concepts)
    difficulty_levels = ['EASY', 'MEDIUM', 'HARD']
    actual_concepts = [c for c in concepts_list if c not in difficulty_levels]
    
    # Print header
    print("\n" + "=" * 80)
    print(colored("Quiz Questions Overview", 'green').center(80))
    print("=" * 80)
    
    # Print difficulty levels
    print("\n" + colored("Difficulty Levels", 'cyan').center(80))
    print("-" * 80)
    for level in difficulty_levels:
        if level in concepts_list:
            print(colored(f"• {level}", 'yellow').center(80))
    
    # Print concepts
    print("\n" + colored("Concepts Covered", 'cyan').center(80))
    print("-" * 80)
    for concept in sorted(actual_concepts):
        print(colored(f"• {concept}", 'yellow').center(80))
    
    print("\n" + "=" * 80)
    print(colored("Questions List", 'green').center(80))
    print("=" * 80)

    # Get all questions for this teacher
    cursor.execute(f"""
        SELECT id, question_text, options, correct_answer, difficulty, concepts 
        FROM {DatabaseConfig.QUESTIONS_TABLE} 
        WHERE teacher_id = %s 
        ORDER BY id
    """, (teacher_id,))
    questions = cursor.fetchall()
    
    if not questions:
        print(colored("\nNo questions found for this teacher.", 'yellow').center(80))
        print("=" * 80 + "\n")
        return
    
    # Print questions
    for i, qn in enumerate(questions, 1):
        id, question_text, options_json, correct_answer, difficulty, concepts_json = qn
        options = json.loads(options_json)
        concepts = json.loads(concepts_json)
        
        # Print question header
        print("\n" + "-" * 80)
        print(colored(f"Question {i}", 'green').center(80))
        print("-" * 80)
        
        # Print question text
        print(colored("Question:", 'cyan'))
        print(question_text)
        print()
        
        # Print options
        print(colored("Options:", 'cyan'))
        for opt in options:
            print(colored(f"• {opt}", 'yellow'))
        print()
        
        # Print correct answer
        print(colored("Correct Answer:", 'green'))
        print(correct_answer)
        print()
        
        # Print concepts
        print(colored("Concepts:", 'blue'))
        print(", ".join(concepts))
        print()
        
        # Print difficulty level
        print(colored("Difficulty:", 'magenta'))
        print(difficulty)
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print(colored(f"Total Questions: {len(questions)}", 'yellow').center(80))
    print("=" * 80 + "\n")

def manage_questions(teacher_id):
    from prettytable import PrettyTable
    connection, cursor = get_db_connection()
    while True:
        # Fetch all questions for this teacher
        cursor.execute(f"SELECT id, question_text, options, correct_answer, difficulty, concepts FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE teacher_id = %s ORDER BY id", (teacher_id,))
        questions = cursor.fetchall()
        if not questions:
            print(colored("No questions found.", 'yellow'))
            return

        # Display questions in a table with sequential numbers
        table = PrettyTable()
        table.field_names = ["Q. No.", "Question", "Difficulty", "Correct", "Concepts"]
        table.max_width = 50  # Set overall max width
        table.hrules = True  # Add horizontal rules between rows
        
        id_map = []  # Maps sequential number to actual id
        for idx, q in enumerate(questions, 1):
            id, question_text, options_json, correct_answer, difficulty, concepts_json = q
            concepts = json.loads(concepts_json)
            
            # Format the question text
            if len(question_text) > 50:
                question_text = question_text[:47] + "..."
            
            # Format concepts
            concepts_str = ", ".join(concepts)
            if len(concepts_str) > 30:
                concepts_str = concepts_str[:27] + "..."
            
            # Add row with formatted data
            table.add_row([
                idx,
                question_text,
                colored(difficulty, 'yellow'),
                colored(correct_answer, 'green'),
                concepts_str
            ])
            id_map.append(id)

        # Print the table with a nice header
        print("\n" + "="*100)
        print(colored("Your Questions", 'green').center(100))
        print("="*100)
        print(table)
        print("="*100)
        
        # Print menu options with better formatting
        print("\n" + colored("Options:", 'cyan'))
        print(colored("1.", 'yellow') + " Edit a question")
        print(colored("2.", 'yellow') + " Delete a question")
        print(colored("3.", 'yellow') + " Back to main menu")
        
        choice = input(colored("\nEnter your choice (1-3): ", 'green'))
        
        if choice == '1':
            qno = input(colored("\nEnter Question Number to edit: ", 'yellow'))
            if not qno.isdigit() or int(qno) < 1 or int(qno) > len(id_map):
                print(colored("Invalid question number.", 'red'))
                continue
                
            qid = id_map[int(qno)-1]
            cursor.execute(f"SELECT id, question_text, options, correct_answer, difficulty, concepts FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE id = %s AND teacher_id = %s", (qid, teacher_id))
            q = cursor.fetchone()
            
            if not q:
                print(colored("Question not found.", 'red'))
                continue
                
            id, question_text, options_json, correct_answer, difficulty, concepts_json = q
            options = json.loads(options_json)
            concepts = json.loads(concepts_json)
            
            print("\n" + "="*80)
            print(colored("Edit Question", 'green').center(80))
            print("="*80)
            print(colored("Current Question:", 'cyan'))
            print(question_text)
            print("\n" + colored("Current Options:", 'cyan'))
            for i, opt in enumerate(options, 1):
                print(f"{i}. {opt}")
            print("\n" + colored("Current Correct Answer:", 'cyan'))
            print(correct_answer)
            print("\n" + colored("Current Difficulty:", 'cyan'))
            print(difficulty)
            print("\n" + colored("Current Concepts:", 'cyan'))
            print(", ".join(concepts))
            print("="*80)
            
            print("\n" + colored("Which field do you want to edit?", 'cyan'))
            print(colored("1.", 'yellow') + " Question Text")
            print(colored("2.", 'yellow') + " Options")
            print(colored("3.", 'yellow') + " Correct Answer")
            print(colored("4.", 'yellow') + " Difficulty")
            print(colored("5.", 'yellow') + " Concepts")
            print(colored("6.", 'yellow') + " Cancel")
            
            field = input(colored("\nEnter your choice (1-6): ", 'green'))
            
            if field == '1':
                new_text = input(colored("\nEnter new question text: ", 'yellow'))
                cursor.execute(f"UPDATE {DatabaseConfig.QUESTIONS_TABLE} SET question_text = %s WHERE id = %s", (new_text, id))
            elif field == '2':
                print(colored("\nCurrent options:", 'cyan'))
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                new_opts = []
                for i in range(1, 5):
                    new_opt = input(colored(f"\nEnter option {i}: ", 'yellow'))
                    new_opts.append(new_opt)
                cursor.execute(f"UPDATE {DatabaseConfig.QUESTIONS_TABLE} SET options = %s WHERE id = %s", (json.dumps(new_opts), id))
            elif field == '3':
                print(colored("\nCurrent options:", 'cyan'))
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                new_corr = input(colored("\nEnter new correct answer (type the full option): ", 'yellow'))
                if new_corr not in options:
                    print(colored("That answer is not in the options.", 'red'))
                    continue
                cursor.execute(f"UPDATE {DatabaseConfig.QUESTIONS_TABLE} SET correct_answer = %s WHERE id = %s", (new_corr, id))
            elif field == '4':
                print(colored("\nCurrent difficulty:", 'cyan'), difficulty)
                print(colored("1.", 'yellow') + " EASY")
                print(colored("2.", 'yellow') + " MEDIUM")
                print(colored("3.", 'yellow') + " HARD")
                new_diff = input(colored("\nEnter new difficulty (1-3): ", 'yellow'))
                if new_diff == '1':
                    new_diff = 'EASY'
                elif new_diff == '2':
                    new_diff = 'MEDIUM'
                elif new_diff == '3':
                    new_diff = 'HARD'
                else:
                    print(colored("Invalid difficulty.", 'red'))
                    continue
                cursor.execute(f"UPDATE {DatabaseConfig.QUESTIONS_TABLE} SET difficulty = %s WHERE id = %s", (new_diff, id))
            elif field == '5':
                print(colored("\nCurrent concepts:", 'cyan'), ', '.join(concepts))
                new_concepts = input(colored("\nEnter new concepts (comma separated): ", 'yellow'))
                new_concepts_list = [c.strip() for c in new_concepts.split(',') if c.strip()]
                cursor.execute(f"UPDATE {DatabaseConfig.QUESTIONS_TABLE} SET concepts = %s WHERE id = %s", (json.dumps(new_concepts_list), id))
            elif field == '6':
                continue
            else:
                print(colored("Invalid choice.", 'red'))
                continue
                
            connection.commit()
            print(colored("\nQuestion updated successfully!", 'green'))
            
        elif choice == '2':
            qno = input(colored("\nEnter Question Number to delete: ", 'yellow'))
            if not qno.isdigit() or int(qno) < 1 or int(qno) > len(id_map):
                print(colored("Invalid question number.", 'red'))
                continue
                
            qid = id_map[int(qno)-1]
            cursor.execute(f"SELECT id FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE id = %s AND teacher_id = %s", (qid, teacher_id))
            if not cursor.fetchone():
                print(colored("Question not found.", 'red'))
                continue
                
            confirm = input(colored("\nAre you sure you want to delete this question? (y/n): ", 'red'))
            if confirm.lower() == 'y':
                cursor.execute(f"DELETE FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE id = %s", (qid,))
                connection.commit()
                print(colored("\nQuestion deleted successfully!", 'green'))
            else:
                print(colored("\nDeletion cancelled.", 'yellow'))
                
        elif choice == '3':
            break
        else:
            print(colored("Invalid choice.", 'red'))

def main(choiceee, CURSOR, connect, passwd=None):
    if choiceee == VM_CHOICE_DATA_VIEW:

        print("Select : ")
        print("1. Admins Data")
        print("2. Students Data")
        print("3. Questions Data")
        print("4. User Statistics")

        choice = input(colored(">> ", 'green'))

        if not choice.isnumeric():
            print("Invalid choice")
        else:
            choice = int(choice)
            if choice == 1:

                print("Admins Data : ")

                CURSOR.execute(f"SELECT * FROM {TEACHERS_DATABASE}")
                admins_table = PrettyTable(["Mentor Name", "Password"])

                data = CURSOR.fetchall()

                for entry in data:
                    admins_table.add_row(entry)

                print(admins_table)

                print('\n\n\n')

            elif choice == 2:

                print("Students Data : ")

                CURSOR.execute(f"SELECT * FROM {STUDENTS_DATABASE}")
                students_table = PrettyTable(["Student Name", "Password", "Mentor Name"])

                data = CURSOR.fetchall()

                for entry in data:
                    students_table.add_row(entry)

                print(students_table)

                print('\n\n\n')

            elif choice == 3:

                view_quiz()

            elif choice == 4:

                print("User Statistics : ")

                with open("data/user_stats.bin", 'rb') as f:
                    data = pickle.load(f)
                    
                    for i in data:
                        print(f"Student Name : {i["User_name"]}")
                        print(f"Mentor Name : {i["Mentor_name"]}")

                        analysises = i["Analysis"]

                        for j, analysis in enumerate(analysises):
                            print(f"Attempt {j + 1}")

                            print("Overall Report : ")
                            data = analysis["overall"]
                            print()

                            overall_data_table = PrettyTable(["Total Questions", "Correct", "Incorrect", "Score"])
                            overall_data_table.add_row([data["correct"] + data["incorrect"], data["correct"], data["incorrect"], f'{analysis["score"]}%'])

                            print(overall_data_table)

                            print()
                            print()

                            data = analysis["q_wise"]
                            print("Question Wise Report")
                            qwise_data_table = PrettyTable(["QID", "Question", "Time", "Accuracy", "Level", "Key Concepts"])
                            for d in data:
                                qwise_data_table.add_row([d["QID"], d["Question"], d["Time"], colored("Correct" if d["Accuracy"] else "Incorrect", 'green' if d["Accuracy"] else 'red'), d["Level"], d["Key Concepts"]])
                                qwise_data_table.add_row(["", "", "", "", "", ""])
                            
                            print(qwise_data_table)

                            print()
                            print()

            else:
                print("Invalid choice")

def init():
    print("Select : ")
    print("1. View Data")
    print("2. Clear Whole Data")
    print("3. Clear Specific Entries")

    choiceee = input(colored(">> ", 'green'))

    if not choiceee.isnumeric():
        print("Invalid Choice")
    else:
        choiceee = int(choiceee)
        CURSOR, connect = init_sql.init()
        main(choiceee, CURSOR, connect)

        init_sql.close()

if __name__ == "__main__":
    init()

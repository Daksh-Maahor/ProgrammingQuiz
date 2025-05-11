import random
import time as time_measure
import colorama
from termcolor import colored
from init_sql import DatabaseConfig, get_db_connection
import json

colorama.init()

# Player name
NAME = ''

QUESTIONS_LIST = None # to be used in program

QUESTIONS_ALL = None # List of all questions

QID_LIST = None

#Total no of questions to be taken out of the database
NUM_QUESTIONS_IN_QUIZ = 10

# QUESTION LEVELS
LEVEL_EASY = 'EASY'
LEVEL_MEDIUM = 'MEDIUM'
LEVEL_HARD = 'HARD'
LEVELS_QUE = [LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD]

# QUESTION TYPES
TYPE_MCQ = 'MCQ'
TYPES_QUE = [TYPE_MCQ]

            
# to load questions
def load_questions(mentor_name):
    global QUESTIONS_LIST, QUESTIONS_ALL, QID_LIST
    QUESTIONS_ALL = []
    connection, cursor = get_db_connection()
    cursor.execute(f"SELECT id, question_text, options, correct_answer, concepts FROM {DatabaseConfig.QUESTIONS_TABLE} WHERE teacher_id = %s", (mentor_name,))
    for row in cursor.fetchall():
        id, question_text, options_json, correct_answer, concepts_json = row
        options = json.loads(options_json)
        concepts = json.loads(concepts_json)
        QUESTIONS_ALL.append({
            'hash': id,
            'question': question_text,
            'options': options,
            'correct_option': correct_answer,
            'concepts': concepts,
            'type': 'MCQ'
        })
    
    QID_LIST = [i['hash'] for i in QUESTIONS_ALL]
    
    l = len(QUESTIONS_ALL)
    
    if l <= NUM_QUESTIONS_IN_QUIZ:
        QUESTIONS_LIST = QUESTIONS_ALL
    else:
        q_list = [i for i in QUESTIONS_ALL]
        QUESTIONS_LIST = []
        
        j = 0 # to keep track of questions taken
        
        while j < NUM_QUESTIONS_IN_QUIZ:
            i = random.randrange(0, len(q_list))
            QUESTIONS_LIST.append(q_list[i])
            
            q_list.pop(i)
            
            random.shuffle(q_list)
            j += 1
    
'Classes'

class Question:
    def __init__(self, question, options, correct_option, concepts, type, hash):
        self.question = question
        self.options = options
        self.correct_option = correct_option
        self.concepts = concepts
        self.type = type
        self.hash = hash

class MCQ(Question):
    def __init__(self, question, options, correct_option, concepts, hash):
        super().__init__(question, options, correct_option, concepts, TYPE_MCQ, hash)

class QuizState:
    def __init__(self, questions):
        self.questions = []
        for q in questions:
            if q['type'] == 'MCQ':
                self.questions.append(MCQ(
                    question=q['question'],
                    options=q['options'],
                    correct_option=q['correct_option'],
                    concepts=q['concepts'],
                    hash=q['hash']
                ))
        self.current_question = 0
        self.score = 0
        self.attempts = []
        # Generate a unique quiz session ID
        connection, cursor = get_db_connection()
        cursor.execute("SELECT MAX(quiz_session_id) FROM quiz_attempts")
        max_session = cursor.fetchone()[0]
        self.quiz_session_id = 1 if max_session is None else max_session + 1

    def next_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def check_answer(self, answer, time_taken):
        question = self.questions[self.current_question]
        is_correct = answer == question.correct_option
        
        # Store attempt in database
        connection, cursor = get_db_connection()
        try:
            cursor.execute("""
                INSERT INTO quiz_attempts 
                (quiz_session_id, student_name, question_id, selected_answer, time_taken) 
                VALUES (%s, %s, %s, %s, %s)
            """, (self.quiz_session_id, NAME, question.hash, answer, time_taken))
            connection.commit()
        except Exception as e:
            print(colored(f"Error saving attempt: {str(e)}", 'red'))
        
        self.attempts.append({
            'question': question.question,
            'answer': answer,
            'correct': is_correct,
            'time': time_taken
        })
        
        if is_correct:
            self.score += 1
        
        self.current_question += 1
        return is_correct

def play(student_name, mentor_name):
    global NAME, QUESTIONS_LIST
    NAME = student_name
    
    load_questions(mentor_name)
    
    if not QUESTIONS_LIST:
        print(colored("No questions available for this teacher.", 'red'))
        return None
    
    quiz = QuizState(QUESTIONS_LIST)
    
    print(colored("Starting Quiz...", 'green'))
    print()
    
    while True:
        question = quiz.next_question()
        if not question:
            break
        
        print(colored("Question:", 'cyan'))
        print(question.question)
        print()
        
        print(colored("Options:", 'yellow'))
        for i, option in enumerate(question.options, 1):
            print(f"{i}. {option}")
        print()
        
        start_time = time_measure.time()
        
        while True:
            try:
                answer = int(input(colored("Enter your answer (1-4): ", 'green')))
                if 1 <= answer <= 4:
                    break
                print(colored("Please enter a number between 1 and 4", 'red'))
            except ValueError:
                print(colored("Please enter a valid number", 'red'))
        
        end_time = time_measure.time()
        time_taken = end_time - start_time
        
        selected_answer = question.options[answer - 1]
        is_correct = quiz.check_answer(selected_answer, time_taken)
        
        print()
        if is_correct:
            print(colored("Correct!", 'green'))
        else:
            print(colored("Incorrect!", 'red'))
            print(colored(f"Correct answer: {question.correct_option}", 'yellow'))
        print()
        
        print(colored(f"Time taken: {time_taken:.2f} seconds", 'cyan'))
        print()
        print("-" * 50)
        print()
    
    score_percentage = (quiz.score / len(QUESTIONS_LIST)) * 100
    print(colored("Quiz completed!", 'green'))
    print(colored(f"Score: {quiz.score}/{len(QUESTIONS_LIST)} ({score_percentage:.1f}%)", 'yellow'))
    print()
    
    return quiz.attempts

if __name__ == "__main__":
    play("", "")
    
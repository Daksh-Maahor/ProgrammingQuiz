import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StudensTableConfig:
    STUDENTS_TABLE = "students_login_data"
    USER_NAME = "USER_NAME"
    PASSWORD = "PASSWD"
    MENTOR_NAME = "MENTOR_NAME"
    TIME_CREATED = "CREATED_AT"

class TeachersTableConfig:
    TEACHERS_TABLE = "teachers_login_data"
    USER_NAME = "USER_NAME"
    PASSWORD = "PASSWD"
    TIME_CREATED = "CREATED_AT"

class QuestionsTableConfig:
    QUESTIONS_TABLE = "questions"
    ID = "ID"
    MENTOR_ID = "MENTOR_ID"
    QUESTION_TEXT = "QUESTION_TEXT"
    OPTIONS = "OPTIONS"
    CORRECT_ANSWER = "CORRECT_ANSWER"
    DIFFICULTY = "DIFFICULTY"
    CONCEPTS = "CONCEPTS"
    CREATED_AT = "CREATED_AT"

class QuizAttemptsTableConfig:
    QUIZ_ATTEMPTS_TABLE = "quiz_attempts"
    QUIZ_SESSION_ID = "QUIZ_SESSION_ID"
    STUDENT_NAME = "STUDENT_NAME"
    MENTOR_NAME = "MENTOR_NAME"
    QUESTION_ID = "QUESTION_ID"
    SELECTED_ANSWER = "SELECTED_ANSWER"
    TIME_TAKEN = "TIME_TAKEN"
    ATTEMPT_DATE = "ATTEMPT_DATE"

class DatabaseConfig:
    """Database configuration class"""
    HOST = os.getenv('DB_HOST', 'localhost')
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = 'programming_quiz'

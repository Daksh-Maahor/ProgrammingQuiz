import mysql.connector as sql
from mysql.connector import Error
from typing import Tuple, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    HOST = os.getenv('DB_HOST', 'localhost')
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = 'programming_quiz'
    STUDENTS_TABLE = "students_login_data"
    TEACHERS_TABLE = "teachers_login_data"
    QUESTIONS_TABLE = "questions"
    QUIZ_ATTEMPTS_TABLE = "quiz_attempts"

class DatabaseConnection:
    """Database connection manager"""
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            self.initialize_connection()

    def initialize_connection(self) -> None:
        """Initialize database connection and cursor"""
        try:
            self._connection = sql.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD
            )
            self._cursor = self._connection.cursor(buffered=True)
            self._create_database()
            self._create_tables()
        except Error as e:
            raise Exception(f"Failed to initialize database connection: {str(e)}")

    def _create_database(self) -> None:
        """Create database if it doesn't exist"""
        try:
            self._cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DATABASE}")
            self._cursor.execute(f"USE {DatabaseConfig.DATABASE}")
        except Error as e:
            raise Exception(f"Failed to create database: {str(e)}")

    def _create_tables(self) -> None:
        """Create necessary tables if they don't exist"""
        try:
            # Create teachers table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DatabaseConfig.TEACHERS_TABLE} (
                    USER_NAME VARCHAR(100) NOT NULL PRIMARY KEY,
                    PASSWD VARCHAR(100) NOT NULL,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create students table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DatabaseConfig.STUDENTS_TABLE} (
                    USER_NAME VARCHAR(100) NOT NULL,
                    PASSWD VARCHAR(100) NOT NULL,
                    MENTOR_NAME VARCHAR(100) NOT NULL,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY(USER_NAME, MENTOR_NAME),
                    FOREIGN KEY(MENTOR_NAME) REFERENCES {DatabaseConfig.TEACHERS_TABLE}(USER_NAME)
                        ON DELETE CASCADE
                )
            """)

            # Create questions table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DatabaseConfig.QUESTIONS_TABLE} (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    MENTOR_ID VARCHAR(100) NOT NULL,
                    QUESTION_TEXT TEXT NOT NULL,
                    OPTIONS JSON NOT NULL,
                    CORRECT_ANSWER VARCHAR(100) NOT NULL,
                    DIFFICULTY ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
                    CONCEPTS JSON NOT NULL,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (teacher_id) REFERENCES {DatabaseConfig.TEACHERS_TABLE}(USER_NAME)
                        ON DELETE CASCADE
                )
            """)

            # Create quiz_attempts table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {DatabaseConfig.QUIZ_ATTEMPTS_TABLE} (
                    ATTEMPT_ID INT AUTO_INCREMENT PRIMARY KEY,
                    QUIZ_SESSION_ID INT NOT NULL,
                    STUDENT_NAME VARCHAR(100) NOT NULL,
                    MENTOR_NAME VARCHAR(100) NOT NULL,
                    QUESTION_ID INT NOT NULL,
                    SELECTED_ANSWER VARCHAR(100) NOT NULL,
                    TIME_TAKEN FLOAT NOT NULL,
                    ATTEMPT_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (STUDENT_NAME, MENTOR_NAME) REFERENCES {DatabaseConfig.STUDENTS_TABLE}(USER_NAME, MENTOR_NAME)
                        ON DELETE CASCADE,
                    FOREIGN KEY (QUESTION_ID) REFERENCES {DatabaseConfig.QUESTIONS_TABLE}(id)
                        ON DELETE CASCADE
                )
            """)

            self._connection.commit()
        except Error as e:
            raise Exception(f"Failed to create tables: {str(e)}")

    def get_connection(self) -> Tuple[sql.MySQLConnection, sql.cursor.MySQLCursor]:
        """Get database connection and cursor"""
        if not self._connection or not self._connection.is_connected():
            self.initialize_connection()
        return self._connection, self._cursor

    def close(self) -> None:
        """Close database connection"""
        if self._cursor:
            self._cursor.close()
        if self._connection and self._connection.is_connected():
            self._connection.close()

# Initialize database connection
db = DatabaseConnection()

def get_db_connection() -> Tuple[sql.MySQLConnection, sql.cursor.MySQLCursor]:
    """Get database connection and cursor"""
    return db.get_connection()

def close_db_connection() -> None:
    """Close database connection"""
    db.close()

if __name__ == "__main__":
    try:
        connection, cursor = get_db_connection()
        print("Database connection successful!")
        close_db_connection()
    except Exception as e:
        print(f"Error: {str(e)}")

import mysql.connector as sql
from mysql.connector import Error
from typing import Tuple
from config import DatabaseConfig, TeachersTableConfig, QuestionsTableConfig, QuizAttemptsTableConfig, StudensTableConfig

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
                CREATE TABLE IF NOT EXISTS {TeachersTableConfig.TEACHERS_TABLE} (
                    {TeachersTableConfig.USER_NAME} VARCHAR(100) NOT NULL PRIMARY KEY,
                    {TeachersTableConfig.PASSWORD} VARCHAR(100) NOT NULL,
                    {TeachersTableConfig.TIME_CREATED} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create students table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {StudensTableConfig.STUDENTS_TABLE} (
                    {StudensTableConfig.USER_NAME} VARCHAR(100) NOT NULL,
                    {StudensTableConfig.PASSWORD} VARCHAR(100) NOT NULL,
                    {StudensTableConfig.MENTOR_NAME} VARCHAR(100) NOT NULL,
                    {StudensTableConfig.TIME_CREATED} TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY({StudensTableConfig.USER_NAME}, {StudensTableConfig.MENTOR_NAME}),
                    FOREIGN KEY({StudensTableConfig.MENTOR_NAME}) REFERENCES {TeachersTableConfig.TEACHERS_TABLE}({TeachersTableConfig.USER_NAME})
                    ON DELETE CASCADE
                )
            """)

            # Create questions table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {QuestionsTableConfig.QUESTIONS_TABLE} (
                    {QuestionsTableConfig.ID} INT AUTO_INCREMENT PRIMARY KEY,
                    {QuestionsTableConfig.MENTOR_ID} VARCHAR(100) NOT NULL,
                    {QuestionsTableConfig.QUESTION_TEXT} TEXT NOT NULL,
                    {QuestionsTableConfig.OPTIONS} JSON NOT NULL,
                    {QuestionsTableConfig.CORRECT_ANSWER} VARCHAR(100) NOT NULL,
                    {QuestionsTableConfig.DIFFICULTY} ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
                    {QuestionsTableConfig.CONCEPTS} JSON NOT NULL,
                    {QuestionsTableConfig.CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY ({QuestionsTableConfig.MENTOR_ID}) REFERENCES {TeachersTableConfig.TEACHERS_TABLE}({TeachersTableConfig.USER_NAME})
                    ON DELETE CASCADE
                )
            """)

            # Create quiz_attempts table
            self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {QuizAttemptsTableConfig.QUIZ_ATTEMPTS_TABLE} (
                    {QuizAttemptsTableConfig.QUIZ_SESSION_ID} INT NOT NULL,
                    {QuizAttemptsTableConfig.STUDENT_NAME} VARCHAR(100) NOT NULL,
                    {QuizAttemptsTableConfig.MENTOR_NAME} VARCHAR(100) NOT NULL,
                    {QuizAttemptsTableConfig.QUESTION_ID} INT NOT NULL,
                    {QuizAttemptsTableConfig.SELECTED_ANSWER} VARCHAR(100) NOT NULL,
                    {QuizAttemptsTableConfig.TIME_TAKEN} FLOAT NOT NULL,
                    {QuizAttemptsTableConfig.ATTEMPT_DATE} TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY ({QuizAttemptsTableConfig.STUDENT_NAME}, {QuizAttemptsTableConfig.MENTOR_NAME}) REFERENCES {StudensTableConfig.STUDENTS_TABLE}({StudensTableConfig.USER_NAME}, {StudensTableConfig.MENTOR_NAME})
                        ON DELETE CASCADE,
                    FOREIGN KEY ({QuizAttemptsTableConfig.QUESTION_ID}) REFERENCES {QuestionsTableConfig.QUESTIONS_TABLE}({QuestionsTableConfig.ID})
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

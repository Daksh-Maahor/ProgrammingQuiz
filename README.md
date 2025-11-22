# Programming Quiz System

A command-line based quiz management system for programming education, built with Python. This system allows teachers to create and manage quizzes, while students can take quizzes and track their progress.

## Features

- **User Authentication**
  - Separate login systems for teachers and students
  - Secure password management
  - Role-based access control

- **Teacher Features**
  - Create and manage quizzes
  - Add questions with multiple choice options
  - Generate unique quiz codes
  - View student performance and statistics
  - Manage question bank

- **Student Features**
  - Take quizzes using unique quiz codes
  - View quiz results and performance
  - Track progress over time

- **Database Management**
  - MySQL database integration
  - Data initialization and management tools
  - Data viewing and clearing capabilities

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Daksh-Maahor/ProgrammingQuiz.git
   cd ProgrammingQuiz
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r text-mode/requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database
   - Configure your database credentials in a `.env` file
   - Run the initialization script:
     ```bash
     python text-mode/init_sql.py
     ```

## Project Structure

- `text-mode/`
  - `main_module.py` - Main entry point
  - `quiz_module.py` - Quiz management functionality
  - `students_module.py` - Student-related operations
  - `teachers_module.py` - Teacher-related operations
  - `common_login_module.py` - Authentication system
  - `init_sql.py` - Database initialization
  - `view_data.py` - Data viewing utilities
  - `add_questions.py` - Question management
  - `clear_data_module.py` - Data management utilities
  - `generate_qcodes.py` - Quiz code generation

## Usage

1. Start the application:
   ```bash
   python text-mode/main_module.py
   ```

2. Follow the on-screen prompts to:
   - Log in as a teacher or student
   - Create or take quizzes
   - Manage questions and view results

## Dependencies

- python-dotenv==1.1.0
- mysql-connector-python==9.3.0
- colorama==0.4.6
- termcolor==2.4.0
- prettytable==3.16.0

## Future Expansion: GUI Mode

The project has potential for expansion to include a GUI-based version alongside the current text-mode implementation. A `gui-mode/` folder could be added to the project structure to house a graphical user interface that provides the same functionality as the text mode but with a modern, user-friendly interface.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

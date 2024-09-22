import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Lab2_435L import Student, Instructor, Course
import csv
import re
from functools import partial
import psycopg2

def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.

    This function attempts to connect to a PostgreSQL database with the specified
    credentials. If the connection fails, an error message is displayed using a QMessageBox.

    Returns:
        conn: A psycopg2 connection object if the connection is successful. Returns `None` if the connection fails.
    """
    try:
        conn = psycopg2.connect(
            dbname="School Management",  # Name of the database
            user="postgres",             # Database user
            password="Talineslim0303$",   # Password for the user
            host="localhost",             # Host address (usually localhost)
            port="5432"                   # Port number for the database connection
        )
        return conn
    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"Failed to connect to the database: {e}")
        return None

def initialize_tables():
    """
    Initializes the necessary database tables for the school management system.

    This function creates the tables 'students', 'instructors', 'courses',
    'registrations', and 'course_assignments' if they do not already exist.
    It uses foreign keys to establish relationships between students, instructors, and courses.

    If the table creation fails, an error message is displayed using a QMessageBox.

    Tables created:
        - students: Stores student information (student_id, name, age, email).
        - instructors: Stores instructor information (instructor_id, name, age, email).
        - courses: Stores course information (course_id, course_name).
        - registrations: Links students to courses using foreign keys (student_id, course_id).
        - course_assignments: Links instructors to courses using foreign keys (instructor_id, course_id).
    """
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                registration_id SERIAL PRIMARY KEY,
                student_id TEXT REFERENCES students(student_id),
                course_id TEXT REFERENCES courses(course_id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course_assignments (
                assignment_id SERIAL PRIMARY KEY,
                instructor_id TEXT REFERENCES instructors(instructor_id),
                course_id TEXT REFERENCES courses(course_id)
            );
        ''')

        conn.commit()
    except Exception as e:
        QMessageBox.critical(None, "Database Error", f"Failed to initialize tables: {e}")
    finally:
        cursor.close()
        conn.close()

class SchoolManagementSystem(QMainWindow):
    """
    A PyQt application for managing school-related operations.

    This system allows managing students, instructors, and courses, as well as
    registering students for courses and assigning instructors to courses. It provides
    a user interface with forms, tables, and buttons for input and navigation.

    Attributes:
        students (list): A list of student records.
        instructors (list): A list of instructor records.
        courses (list): A list of course records.
        student_count (int): A counter for the number of students.
        instructor_count (int): A counter for the number of instructors.
        course_count (int): A counter for the number of courses.
    """

    def __init__(self):
        """
        Initializes the School Management System GUI.

        The method sets up the main window, layouts, and user interface components, 
        including forms for adding students, instructors, courses, and dashboards 
        showing the count of each entity. It also sets up the table and search functionalities.
        """
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.students = []  # Holds student records
        self.instructors = []  # Holds instructor records
        self.courses = []  # Holds course records

        # Add forms for adding and managing records
        self.add_student_form()
        self.add_instructor_form()
        self.add_course_form()

        # Add registration and assignment forms
        self.add_student_course_registration_form()
        self.add_instructor_course_assignment_form()

        # Create table to display records
        self.create_record_table()

        # Add search functionality for records
        self.add_search_functionality()

        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 2)
        self.main_widget.setLayout(self.layout)

        # Initialize counters for students, instructors, and courses
        self.student_count = 0
        self.instructor_count = 0
        self.course_count = 0

        # Create dashboard to show counts
        self.dashboard_layout = QHBoxLayout()
        self.student_count_label = QLabel("Students: 0")
        self.instructor_count_label = QLabel("Instructors: 0")
        self.course_count_label = QLabel("Courses: 0")

        # Style the dashboard labels
        self.style_dashboard_label(self.student_count_label)
        self.style_dashboard_label(self.instructor_count_label)
        self.style_dashboard_label(self.course_count_label)

        self.dashboard_layout.addWidget(self.student_count_label)
        self.dashboard_layout.addWidget(self.instructor_count_label)
        self.dashboard_layout.addWidget(self.course_count_label)
        self.left_layout.addLayout(self.dashboard_layout)

        # Apply styles to the GUI components
        self.set_styles()
        
        # Add buttons for saving and loading records
        self.add_save_load_buttons()

    def style_dashboard_label(self, label):
        """
        Styles the dashboard label for student, instructor, and course counts.

        The method sets the alignment, font, and appearance (background color, text color, padding, etc.)
        of the label used to display the entity counts on the dashboard.

        Args:
            label (QLabel): The label widget to be styled.
        """
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Arial', 16, QFont.Bold))
        label.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            margin: 10px;
            border-radius: 10px;
        """)

    def set_styles(self):
        """
        Applies custom styles to the PyQt components using a stylesheet.

        The method defines the look and feel of various widgets such as `QPushButton`, 
        `QLineEdit`, `QLabel`, `QComboBox`, and `QTableWidget`. It sets the background colors, 
        borders, font sizes, padding, and hover effects for the components.
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: 1px solid #007bff;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QLabel {
                font-family: Arial;
                font-size: 14px;
                color: #333;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #ccc;
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)


    def add_save_load_buttons(self):
        """
        Adds buttons for saving, loading, exporting data, and backing up the database to the GUI.
    
        This method creates four buttons: 'Save Data', 'Load Data', 'Export to CSV', and 'Backup Database'.
        Each button is styled individually and connected to their respective functions:
        - `save_data()`: Saves current data.
        - `load_data()`: Loads data from a file or database.
        - `export_to_csv()`: Exports the data to a CSV file.
        - `backup_database()`: Backs up the database.
    
        The buttons are added to the left layout of the main window.
    
        The method also applies custom styles for each button to define the background color, font weight, and padding.
    
        Buttons:
            - Save Data: Green background (`#28a745`)
            - Load Data: Blue background (`#17a2b8`)
            - Export to CSV: Orange background with bold text (`#ff9800`)
            - Backup Database: Dark orange background (`#e67e22`)
        """
        save_button = QPushButton("Save Data")
        load_button = QPushButton("Load Data")
        export_button = QPushButton("Export to CSV") 
        backup_button = QPushButton("Backup Database")  
        
        save_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px; padding: 10px;")
        load_button.setStyleSheet("background-color: #17a2b8; color: white; border-radius: 5px; padding: 10px;")
        export_button.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold; padding: 10px 15px; border-radius: 5px;")
        backup_button.setStyleSheet("background-color: #e67e22; color: white; padding: 10px 15px; border-radius: 5px;")  # New style for backup button
        
        # Connect buttons to their respective functions
        save_button.clicked.connect(self.save_data)
        load_button.clicked.connect(self.load_data)
        export_button.clicked.connect(self.export_to_csv)
        backup_button.clicked.connect(self.backup_database)
        
        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(backup_button)
        
        # Add the button layout to the left layout of the main window
        self.left_layout.addLayout(button_layout)
    

    def add_student_form(self):
        """
        Creates and adds a form for adding student details to the GUI.
    
        The form includes fields for entering the student's name, age, email, and ID. 
        An 'Add Student' button is also provided, which, when clicked, triggers the `add_student()` method.
    
        Fields:
            - Student Name: A QLineEdit for the student's name.
            - Student Age: A QLineEdit for the student's age.
            - Student Email: A QLineEdit for the student's email.
            - Student ID: A QLineEdit for the student's unique ID.
        """
        student_form = QFormLayout()
    
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()  
        self.student_id_input = QLineEdit()
    
        student_form.addRow(QLabel("Student Name:"), self.student_name_input)
        student_form.addRow(QLabel("Student Age:"), self.student_age_input)
        student_form.addRow(QLabel("Student Email:"), self.student_email_input) 
        student_form.addRow(QLabel("Student ID:"), self.student_id_input)
    
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
    
        self.left_layout.addLayout(student_form)
        self.left_layout.addWidget(add_student_button)
    
    def add_instructor_form(self):
        """
        Creates and adds a form for adding instructor details to the GUI.
    
        The form includes fields for entering the instructor's name, age, email, and ID.
        An 'Add Instructor' button is provided, which, when clicked, triggers the `add_instructor()` method.
    
        Fields:
            - Instructor Name: A QLineEdit for the instructor's name.
            - Instructor Age: A QLineEdit for the instructor's age.
            - Instructor Email: A QLineEdit for the instructor's email.
            - Instructor ID: A QLineEdit for the instructor's unique ID.
        """
        instructor_form = QFormLayout()
    
        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit() 
        self.instructor_id_input = QLineEdit()
    
        instructor_form.addRow(QLabel("Instructor Name:"), self.instructor_name_input)
        instructor_form.addRow(QLabel("Instructor Age:"), self.instructor_age_input)
        instructor_form.addRow(QLabel("Instructor Email:"), self.instructor_email_input)  
        instructor_form.addRow(QLabel("Instructor ID:"), self.instructor_id_input)
    
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
    
        self.left_layout.addLayout(instructor_form)
        self.left_layout.addWidget(add_instructor_button)
    
    def add_course_form(self):
        """
        Creates and adds a form for adding course details to the GUI.
    
        The form includes fields for entering the course ID and course name.
        An 'Add Course' button is provided, which, when clicked, triggers the `add_course()` method.
    
        Fields:
            - Course ID: A QLineEdit for the course's unique ID.
            - Course Name: A QLineEdit for the course's name.
        """
        course_form = QFormLayout()
    
        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()
    
        course_form.addRow(QLabel("Course ID:"), self.course_id_input)
        course_form.addRow(QLabel("Course Name:"), self.course_name_input)
    
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
    
        self.left_layout.addLayout(course_form)
        self.left_layout.addWidget(add_course_button)
    
    def add_student_course_registration_form(self):
        """
        Creates and adds a form for registering students for courses.
    
        The form includes a dropdown to select a student and a dropdown to select a course.
        A 'Register Student for Course' button is provided, which, when clicked, triggers the 
        `register_student_for_course()` method.
    
        Fields:
            - Select Student: A QComboBox for selecting a student.
            - Select Course: A QComboBox for selecting a course.
        """
        student_registration_form = QFormLayout()
    
        self.student_combobox = QComboBox()
        self.student_combobox.addItem("Select a Student")
    
        self.course_combobox_for_registration = QComboBox()
        self.course_combobox_for_registration.addItem("Select a Course")
    
        student_registration_form.addRow(QLabel("Select Student:"), self.student_combobox)
        student_registration_form.addRow(QLabel("Select Course:"), self.course_combobox_for_registration)
    
        register_student_button = QPushButton("Register Student for Course")
        register_student_button.clicked.connect(self.register_student_for_course)
    
        self.left_layout.addLayout(student_registration_form)
        self.left_layout.addWidget(register_student_button)
    
    def add_instructor_course_assignment_form(self):
        """
        Creates and adds a form for assigning instructors to courses.
    
        The form includes a dropdown to select an instructor and a dropdown to select a course.
        An 'Assign Instructor to Course' button is provided, which, when clicked, triggers the
        `assign_instructor_to_course()` method.
    
        Fields:
            - Select Instructor: A QComboBox for selecting an instructor.
            - Select Course: A QComboBox for selecting a course.
        """
        instructor_assignment_form = QFormLayout()
    
        self.instructor_combobox = QComboBox()
        self.instructor_combobox.addItem("Select an Instructor")
    
        self.course_combobox_for_assignment = QComboBox()
        self.course_combobox_for_assignment.addItem("Select a Course")
    
        instructor_assignment_form.addRow(QLabel("Select Instructor:"), self.instructor_combobox)
        instructor_assignment_form.addRow(QLabel("Select Course:"), self.course_combobox_for_assignment)
    
        assign_instructor_button = QPushButton("Assign Instructor to Course")
        assign_instructor_button.clicked.connect(self.assign_instructor_to_course)
    
        self.left_layout.addLayout(instructor_assignment_form)
        self.left_layout.addWidget(assign_instructor_button)

    def add_search_functionality(self):
        """
        Adds search functionality to the GUI.
    
        This method creates a search input field and a filter dropdown for searching 
        through records by name, ID, or course. A 'Search' button is also provided, which 
        triggers the `search_records()` method when clicked.
    
        Fields:
            - Search: A QLineEdit for entering search terms.
            - Filter by: A QComboBox to select the search filter (by Name, ID, or Course).
        """
        search_layout = QFormLayout()
    
        self.search_input = QLineEdit()
        self.search_combobox = QComboBox()
        self.search_combobox.addItems(["Search by Name", "Search by ID", "Search by Course"])
    
        search_layout.addRow(QLabel("Search:"), self.search_input)
        search_layout.addRow(QLabel("Filter by:"), self.search_combobox)
    
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
    
        self.right_layout.addLayout(search_layout)
        self.right_layout.addWidget(search_button)
    
    def add_student(self):
        """
        Adds a new student to the system and the database.
    
        This method collects the student's name, age, email, and ID from input fields.
        It validates the inputs and then inserts the new student into the database. 
        The student is also added to the in-memory list and the student dropdown for course registration.
    
        Input validation:
            - Name: Must contain only alphabetic characters.
            - Age: Must be a positive integer.
            - Email: Must be a valid email format.
        
        Updates:
            - Adds the student to the students list and increments the student count.
            - Updates the student count label and refreshes the student table.
    
        Error Handling:
            - Displays error messages for invalid inputs or database failures.
        """
        name = self.student_name_input.text().strip()
        age = self.student_age_input.text().strip()
        email = self.student_email_input.text().strip()
        student_id = self.student_id_input.text().strip()
    
        if not name.isalpha() or not age.isdigit() or int(age) <= 0 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Input Error", "Please ensure valid inputs for all fields.")
            return
    
        conn = connect_to_db()
        if not conn:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute('''
                INSERT INTO students (student_id, name, age, email)
                VALUES (%s, %s, %s, %s)
            ''', (student_id, name, int(age), email))
    
            conn.commit()
    
            self.students.append(Student(name, int(age), email, student_id))
            self.student_combobox.addItem(name)
            self.student_count += 1
            self.student_count_label.setText(f"Students: {self.student_count}")
            self.update_table()
            self.clear_student_form()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to add student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def add_instructor(self):
        """
        Adds a new instructor to the system and the database.
    
        This method collects the instructor's name, age, email, and ID from input fields.
        It validates the inputs and then inserts the new instructor into the database.
        The instructor is also added to the in-memory list and the instructor dropdown for course assignments.
    
        Input validation:
            - Name: Must contain only alphabetic characters.
            - Age: Must be a positive integer.
            - Email: Must be a valid email format.
        
        Updates:
            - Adds the instructor to the instructors list and increments the instructor count.
            - Updates the instructor count label and refreshes the instructor table.
    
        Error Handling:
            - Displays error messages for invalid inputs or database failures.
        """
        name = self.instructor_name_input.text().strip()
        age = self.instructor_age_input.text().strip()
        email = self.instructor_email_input.text().strip()
        instructor_id = self.instructor_id_input.text().strip()
    
        if not name.isalpha() or not age.isdigit() or int(age) <= 0 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Input Error", "Please ensure valid inputs for all fields.")
            return
    
        conn = connect_to_db()
        if not conn:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute('''
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (%s, %s, %s, %s)
            ''', (instructor_id, name, int(age), email))
    
            conn.commit()
    
            self.instructors.append(Instructor(name, int(age), email, instructor_id))
            self.instructor_combobox.addItem(name)
            self.instructor_count += 1
            self.instructor_count_label.setText(f"Instructors: {self.instructor_count}")
            self.update_table()
            self.clear_instructor_form()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to add instructor: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def add_course(self):
        """
        Adds a new course to the system and the database.
    
        This method collects the course ID and course name from input fields.
        It validates the inputs and then inserts the new course into the database.
        The course is also added to the in-memory list and the course dropdown for registration and assignments.
    
        Input validation:
            - Course ID: Must not be empty.
            - Course Name: Must not be empty.
        
        Updates:
            - Adds the course to the courses list and increments the course count.
            - Updates the course count label and refreshes the course table.
    
        Error Handling:
            - Displays error messages for invalid inputs or database failures.
        """
        course_id = self.course_id_input.text().strip()
        course_name = self.course_name_input.text().strip()
    
        if not course_id or not course_name:
            QMessageBox.warning(self, "Input Error", "All course fields must be filled!")
            return
    
        conn = connect_to_db()
        if not conn:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute('''
                INSERT INTO courses (course_id, course_name)
                VALUES (%s, %s)
            ''', (course_id, course_name))
    
            conn.commit()
    
            self.courses.append(Course(course_id, course_name))
            self.course_combobox_for_registration.addItem(course_name)
            self.course_combobox_for_assignment.addItem(course_name)
            self.course_count += 1
            self.course_count_label.setText(f"Courses: {self.course_count}")
            self.update_table()
            self.clear_course_form()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to add course: {e}")
        finally:
            cursor.close()
            conn.close()
            
    def register_student_for_course(self):
        """
        Registers a selected student for a selected course.
    
        This method retrieves the selected student and course from the comboboxes, validates the selection, 
        and inserts the registration into the database. It also provides feedback to the user about the success or 
        failure of the operation.
    
        Validation:
            - Ensures both a student and a course are selected before attempting registration.
    
        Database Operations:
            - Retrieves the student's ID based on the selected name from the database.
            - Retrieves the course's ID based on the selected course name from the database.
            - Inserts the student-course registration into the 'registrations' table.
    
        Error Handling:
            - Displays warnings if no student or course is selected.
            - Catches database errors and provides feedback if the registration fails.
    
        Success:
            - Displays a success message when the student is successfully registered for the course.
        """
        student_name = self.student_combobox.currentText()
        course_name = self.course_combobox_for_registration.currentText()
    
        if student_name == "Select a Student" or course_name == "Select a Course":
            QMessageBox.warning(self, "Input Error", "Please select both a student and a course!")
            return
    
        conn = connect_to_db()
        if not conn:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT student_id FROM students WHERE name = %s', (student_name,))
            student_id = cursor.fetchone()[0]
    
            cursor.execute('SELECT course_id FROM courses WHERE course_name = %s', (course_name,))
            course_id = cursor.fetchone()[0]
    
            cursor.execute('''
                INSERT INTO registrations (student_id, course_id)
                VALUES (%s, %s)
            ''', (student_id, course_id))
    
            conn.commit()
            QMessageBox.information(self, "Success", f"Student '{student_name}' registered for '{course_name}' successfully.")
            self.update_table()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to register student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def assign_instructor_to_course(self):
        """
        Assigns a selected instructor to a selected course.
    
        This method retrieves the selected instructor and course from the comboboxes, validates the selection, 
        and inserts the instructor-course assignment into the database. It also provides feedback to the user 
        about the success or failure of the operation.
    
        Validation:
            - Ensures both an instructor and a course are selected before attempting the assignment.
    
        Database Operations:
            - Retrieves the instructor's ID based on the selected name from the database.
            - Retrieves the course's ID based on the selected course name from the database.
            - Inserts the instructor-course assignment into the 'course_assignments' table.
    
        Error Handling:
            - Displays warnings if no instructor or course is selected.
            - Handles errors if the instructor or course is not found in the database.
            - Catches database errors and provides feedback if the assignment fails.
    
        Success:
            - Displays a success message when the instructor is successfully assigned to the course.
        """
        instructor_name = self.instructor_combobox.currentText()
        course_name = self.course_combobox_for_assignment.currentText()
    
        if instructor_name == "Select an Instructor" or course_name == "Select a Course":
            QMessageBox.warning(self, "Input Error", "Please select both an instructor and a course!")
            return
    
        conn = connect_to_db()
        if not conn:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT instructor_id FROM instructors WHERE name = %s', (instructor_name,))
            instructor_id = cursor.fetchone()
            if not instructor_id:
                raise ValueError("Instructor not found in the database.")
    
            cursor.execute('SELECT course_id FROM courses WHERE course_name = %s', (course_name,))
            course_id = cursor.fetchone()
            if not course_id:
                raise ValueError("Course not found in the database.")
    
            cursor.execute('''
                INSERT INTO course_assignments (instructor_id, course_id)
                VALUES (%s, %s)
            ''', (instructor_id[0], course_id[0]))
    
            conn.commit()
            QMessageBox.information(self, "Success", f"Instructor '{instructor_name}' assigned to '{course_name}' successfully.")
            self.update_table()  
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Failed to assign instructor: {e}")
        finally:
            cursor.close()
            conn.close()

    
    def edit_record(self):
        """
        Edits the currently selected record in the table.
    
        This method checks if a record is selected in the table, and based on the entity type (Student, Instructor, or Course), 
        it calls the appropriate edit method (`edit_student()`, `edit_instructor()`, or `edit_course()`).
    
        Validation:
            - Ensures a record is selected in the table before attempting to edit.
    
        Entity Types:
            - Student: Calls `edit_student()` to edit a student record.
            - Instructor: Calls `edit_instructor()` to edit an instructor record.
            - Course: Calls `edit_course()` to edit a course record.
    
        Error Handling:
            - Displays a warning if no record is selected.
        """
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a record to edit.")
            return
    
        entity_type = self.table_widget.item(selected_row, 1).text()
    
        if entity_type == "Student":
            self.edit_student(selected_row)
        elif entity_type == "Instructor":
            self.edit_instructor(selected_row)
        elif entity_type == "Course":
            self.edit_course(selected_row)
    
    def delete_record(self):
        """
        Deletes the currently selected record in the table.
    
        This method checks if a record is selected in the table, and based on the entity type (Student, Instructor, or Course), 
        it calls the appropriate delete method (`delete_student()`, `delete_instructor()`, or `delete_course()`).
    
        Validation:
            - Ensures a record is selected in the table before attempting to delete.
    
        Entity Types:
            - Student: Calls `delete_student()` to delete a student record.
            - Instructor: Calls `delete_instructor()` to delete an instructor record.
            - Course: Calls `delete_course()` to delete a course record.
    
        Error Handling:
            - Displays a warning if no record is selected.
        """
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a record to delete.")
            return
    
        entity_type = self.table_widget.item(selected_row, 1).text()
    
        if entity_type == "Student":
            self.delete_student(selected_row)
        elif entity_type == "Instructor":
            self.delete_instructor(selected_row)
        elif entity_type == "Course":
            self.delete_course(selected_row)
    
    def save_data(self):
        """
        Saves the current system data (students, instructors, and courses) to a JSON file.
    
        This method opens a file dialog for the user to select a location to save the JSON file. It queries the database to 
        retrieve the current students, instructors, and courses, formats the data, and saves it to the selected file.
    
        Operations:
            - Retrieves all student, instructor, and course records from the database.
            - Formats the data into dictionaries.
            - Saves the data as a JSON file at the selected location.
    
        Error Handling:
            - Displays an error message if the data cannot be saved due to a database or file I/O error.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)", options=options)
    
        if file_path:
            conn = connect_to_db()
            if not conn:
                return
            cursor = conn.cursor()
    
            try:
                cursor.execute('SELECT * FROM students')
                students = cursor.fetchall()
                student_list = [{"student_id": s[0], "name": s[1], "age": s[2], "email": s[3]} for s in students]
    
                cursor.execute('SELECT * FROM instructors')
                instructors = cursor.fetchall()
                instructor_list = [{"instructor_id": i[0], "name": i[1], "age": i[2], "email": i[3]} for i in instructors]
    
                cursor.execute('SELECT * FROM courses')
                courses = cursor.fetchall()
                course_list = [{"course_id": c[0], "course_name": c[1]} for c in courses]
    
                data = {
                    "students": student_list,
                    "instructors": instructor_list,
                    "courses": course_list
                }
    
                with open(file_path, 'w') as file:
                    json.dump(data, file)
    
                QMessageBox.information(self, "Success", "Data saved to JSON file successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save data: {e}")
            finally:
                cursor.close()
                conn.close()
    
    def load_data(self):
        """
        Loads system data (students, instructors, and courses) from the database.
    
        This method clears the current data and then queries the database for students, instructors, and courses. 
        The retrieved data is used to populate the in-memory lists, comboboxes, and table.
    
        Operations:
            - Retrieves all student, instructor, and course records from the database.
            - Populates the in-memory student, instructor, and course lists.
            - Updates the comboboxes for course registration and assignments.
            - Updates the student, instructor, and course counts.
    
        Error Handling:
            - Displays an error message if the data cannot be loaded due to a database error.
        """
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            self.students = []
            self.instructors = []
            self.courses = []
            self.student_combobox.clear()
            self.instructor_combobox.clear()
            self.course_combobox_for_registration.clear()
            self.course_combobox_for_assignment.clear()
    
            cursor.execute("SELECT * FROM students")
            for student in cursor.fetchall():
                new_student = Student(student[1], student[2], student[3], student[0])  # (name, age, email, student_id)
                self.students.append(new_student)
                self.student_combobox.addItem(new_student.name)
    
            cursor.execute("SELECT * FROM instructors")
            for instructor in cursor.fetchall():
                new_instructor = Instructor(instructor[1], instructor[2], instructor[3], instructor[0])  # (name, age, email, instructor_id)
                self.instructors.append(new_instructor)
                self.instructor_combobox.addItem(new_instructor.name)
    
            cursor.execute("SELECT * FROM courses")
            for course in cursor.fetchall():
                new_course = Course(course[0], course[1])  # (course_id, course_name)
                cursor.execute("SELECT student_id FROM registrations WHERE course_id = %s", (course[0],))
                for student_id in cursor.fetchall():
                    student = next((s for s in self.students if s.student_id == student_id[0]), None)
                    if student:
                        new_course.add_student(student)
    
                cursor.execute("SELECT instructor_id FROM course_assignments WHERE course_id = %s", (course[0],))
                instructor_id = cursor.fetchone()
                if instructor_id:
                    instructor = next((i for i in self.instructors if i.instructor_id == instructor_id[0]), None)
                    if instructor:
                        new_course.assign_instructor(instructor)
    
                self.courses.append(new_course)
                self.course_combobox_for_registration.addItem(new_course.course_name)
                self.course_combobox_for_assignment.addItem(new_course.course_name)
    
            self.update_student_count()
            self.update_instructor_count()
            self.update_course_count()
    
            self.update_table()
    
            QMessageBox.information(self, "Success", "Data loaded successfully from the database.")
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
    
        finally:
            cursor.close()
            conn.close()
    
        
    def update_student_count(self):
        """
        Updates the student count based on the number of students in the system.
    
        This method calculates the current number of students in the system by counting 
        the entries in the `students` list. It then updates the student count label in the GUI.
        """
        self.student_count = len(self.students)
        self.student_count_label.setText(f"Students: {self.student_count}")
    
    def update_instructor_count(self):
        """
        Updates the instructor count based on the number of instructors in the system.
    
        This method calculates the current number of instructors in the system by counting 
        the entries in the `instructors` list. It then updates the instructor count label in the GUI.
        """
        self.instructor_count = len(self.instructors)
        self.instructor_count_label.setText(f"Instructors: {self.instructor_count}")
    
    def update_course_count(self):
        """
        Updates the course count based on the number of courses in the system.
    
        This method calculates the current number of courses in the system by counting 
        the entries in the `courses` list. It then updates the course count label in the GUI.
        """
        self.course_count = len(self.courses)
        self.course_count_label.setText(f"Courses: {self.course_count}")
    
    def create_record_table(self):
        """
        Creates the table widget for displaying student, instructor, and course records.
    
        This method sets up the table with 7 columns: Name, Type, ID, Age, Instructor/Students, Edit, and Delete.
        The table is added to the right layout of the main window.
    
        Columns:
            - Name: Displays the name of the student, instructor, or course.
            - Type: Specifies the entity type (Student, Instructor, or Course).
            - ID: Displays the unique identifier for the entity.
            - Age: Displays the age of students and instructors, "N/A" for courses.
            - Instructor/Students: Displays the associated instructor and students for a course, or "N/A" for students and instructors.
            - Edit: Provides an "Edit" button to edit the record.
            - Delete: Provides a "Delete" button to delete the record.
        """
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7) 
        self.table_widget.setHorizontalHeaderLabels(["Name", "Type", "ID", "Age", "Instructor/Students", "Edit", "Delete"])
        self.right_layout.addWidget(self.table_widget)
    
    def update_table(self):
        """
        Updates the table with the latest data for students, instructors, and courses.
    
        This method retrieves all student, instructor, and course records from the database and populates the table with the data. 
        Each row represents a record, with "Edit" and "Delete" buttons for each entity (students, instructors, and courses).
    
        Database Operations:
            - Retrieves all student records and adds them to the table.
            - Retrieves all instructor records and adds them to the table.
            - Retrieves all course records and adds them to the table, including the associated instructor and students.
    
        Error Handling:
            - Displays an error message if data retrieval fails.
        """
        self.table_widget.setRowCount(0)  
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            # Fetch and display students
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            for row_position, student in enumerate(students):
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(student[1]))  # Student name
                self.table_widget.setItem(row_position, 1, QTableWidgetItem("Student"))  # Type: Student
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(student[0]))  # Student ID
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(student[2])))  # Student age
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("N/A"))  # Instructor/Students: N/A for students
    
                edit_button = QPushButton("Edit")
                delete_button = QPushButton("Delete")
                edit_button.setStyleSheet("background-color: #ffeb3b; color: black; border-radius: 5px; padding: 5px;")
                delete_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 5px;")
                edit_button.clicked.connect(partial(self.start_editing_student, row_position))
                delete_button.clicked.connect(partial(self.delete_student, row_position))
                self.table_widget.setCellWidget(row_position, 5, edit_button)
                self.table_widget.setCellWidget(row_position, 6, delete_button)
    
            # Fetch and display instructors
            cursor.execute('SELECT * FROM instructors')
            instructors = cursor.fetchall()
            for row_position, instructor in enumerate(instructors, start=len(students)):
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(instructor[1]))  # Instructor name
                self.table_widget.setItem(row_position, 1, QTableWidgetItem("Instructor"))  # Type: Instructor
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(instructor[0]))  # Instructor ID
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(instructor[2])))  # Instructor age
                self.table_widget.setItem(row_position, 4, QTableWidgetItem("N/A"))  # Instructor/Students: N/A for instructors
    
                edit_button = QPushButton("Edit")
                delete_button = QPushButton("Delete")
                edit_button.setStyleSheet("background-color: #ffeb3b; color: black; border-radius: 5px; padding: 5px;")
                delete_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 5px;")
                edit_button.clicked.connect(partial(self.start_editing_instructor, row_position))
                delete_button.clicked.connect(partial(self.delete_instructor, row_position))
                self.table_widget.setCellWidget(row_position, 5, edit_button)
                self.table_widget.setCellWidget(row_position, 6, delete_button)
    
            # Fetch and display courses
            cursor.execute('SELECT * FROM courses')
            courses = cursor.fetchall()
            for row_position, course in enumerate(courses, start=len(students) + len(instructors)):
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(course[1]))  # Course name
                self.table_widget.setItem(row_position, 1, QTableWidgetItem("Course"))  # Type: Course
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(course[0]))  # Course ID
                self.table_widget.setItem(row_position, 3, QTableWidgetItem("N/A"))  # Age: N/A for courses
    
                # Retrieve the associated instructor and students for the course
                cursor.execute('''
                    SELECT i.name FROM instructors i
                    JOIN course_assignments ca ON i.instructor_id = ca.instructor_id
                    WHERE ca.course_id = %s
                ''', (course[0],))
                instructor = cursor.fetchone()
                instructor_name = instructor[0] if instructor else "N/A"
    
                cursor.execute('''
                    SELECT s.name FROM students s
                    JOIN registrations r ON s.student_id = r.student_id
                    WHERE r.course_id = %s
                ''', (course[0],))
                students_in_course = [row[0] for row in cursor.fetchall()]
                student_names = ", ".join(students_in_course) if students_in_course else "No students"
    
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(f"Instructor: {instructor_name}, Students: {student_names}"))
    
                edit_button = QPushButton("Edit")
                delete_button = QPushButton("Delete")
                edit_button.setStyleSheet("background-color: #ffeb3b; color: black; border-radius: 5px; padding: 5px;")
                delete_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 5px;")
                edit_button.clicked.connect(partial(self.start_editing_course, row_position))
                delete_button.clicked.connect(partial(self.delete_course, row_position))
                self.table_widget.setCellWidget(row_position, 5, edit_button)
                self.table_widget.setCellWidget(row_position, 6, delete_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load data: {e}")
        finally:
            cursor.close()
            conn.close()


    def start_editing_student(self, selected_row):
        """
        Loads the selected student's data into the input fields for editing.
    
        This method retrieves the student ID from the selected row in the table, queries the database 
        for the student's information, and populates the student input fields with the retrieved data. 
        It also adds an "Update Student" button to allow the user to save the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the student data cannot be loaded from the database.
        """
        student_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
            student = cursor.fetchone()
    
            if student:
                self.student_name_input.setText(student[1])
                self.student_age_input.setText(str(student[2]))
                self.student_email_input.setText(student[3])
                self.student_id_input.setText(student[0])
    
                self.update_button = QPushButton("Update Student")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_student, student_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def update_student(self, student_id):
        """
        Updates the student's information in the database based on the input fields.
    
        This method retrieves the updated student information from the input fields and updates the corresponding 
        student record in the database. It also refreshes the table and clears the form upon successful update.
    
        Arguments:
            student_id (str): The ID of the student to be updated.
    
        Error Handling:
            - Displays an error message if the student update fails.
        """
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            name = self.student_name_input.text()
            age = int(self.student_age_input.text())
            email = self.student_email_input.text()
            new_student_id = self.student_id_input.text()
    
            cursor.execute('''
                UPDATE students SET student_id = %s, name = %s, age = %s, email = %s WHERE student_id = %s
            ''', (new_student_id, name, age, email, student_id))
    
            conn.commit()
            QMessageBox.information(self, "Success", "Student updated successfully!")
            self.update_table()  
            self.clear_student_form()
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def start_editing_instructor(self, selected_row):
        """
        Loads the selected instructor's data into the input fields for editing.
    
        This method retrieves the instructor ID from the selected row in the table, queries the database 
        for the instructor's information, and populates the instructor input fields with the retrieved data. 
        It also adds an "Update Instructor" button to allow the user to save the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the instructor data cannot be loaded from the database.
        """
        instructor_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM instructors WHERE instructor_id = %s', (instructor_id,))
            instructor = cursor.fetchone()
    
            if instructor:
                self.instructor_name_input.setText(instructor[1])
                self.instructor_age_input.setText(str(instructor[2]))
                self.instructor_email_input.setText(instructor[3])
                self.instructor_id_input.setText(instructor[0])
    
                self.update_button = QPushButton("Update Instructor")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_instructor, instructor_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load instructor: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def update_instructor(self, instructor_id):
        """
        Updates the instructor's information in the database based on the input fields.
    
        This method retrieves the updated instructor information from the input fields and updates the corresponding 
        instructor record in the database. It also refreshes the table and clears the form upon successful update.
    
        Arguments:
            instructor_id (str): The ID of the instructor to be updated.
    
        Error Handling:
            - Displays an error message if the instructor update fails.
        """
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            name = self.instructor_name_input.text()
            age = int(self.instructor_age_input.text())
            email = self.instructor_email_input.text()
            new_instructor_id = self.instructor_id_input.text()
    
            cursor.execute('''
                UPDATE instructors SET instructor_id = %s, name = %s, age = %s, email = %s WHERE instructor_id = %s
            ''', (new_instructor_id, name, age, email, instructor_id))
    
            conn.commit()
            QMessageBox.information(self, "Success", "Instructor updated successfully!")
            self.update_table()  
            self.clear_instructor_form()
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update instructor: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def start_editing_course(self, selected_row):
        """
        Loads the selected course's data into the input fields for editing.
    
        This method retrieves the course ID from the selected row in the table, queries the database 
        for the course's information, and populates the course input fields with the retrieved data. 
        It also adds an "Update Course" button to allow the user to save the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the course data cannot be loaded from the database.
        """
        course_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
            course = cursor.fetchone()
    
            if course:
                self.course_name_input.setText(course[1])
                self.course_id_input.setText(course[0])
    
                self.update_button = QPushButton("Update Course")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_course, course_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load course: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def update_course(self, course_id):
        """
        Updates the course's information in the database based on the input fields.
    
        This method retrieves the updated course information from the input fields and updates the corresponding 
        course record in the database. It also refreshes the table and clears the form upon successful update.
    
        Arguments:
            course_id (str): The ID of the course to be updated.
    
        Error Handling:
            - Displays an error message if the course update fails.
        """
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            course_name = self.course_name_input.text()
            new_course_id = self.course_id_input.text()
    
            cursor.execute('''
                UPDATE courses SET course_id = %s, course_name = %s WHERE course_id = %s
            ''', (new_course_id, course_name, course_id))
    
            conn.commit()
            QMessageBox.information(self, "Success", "Course updated successfully!")
            self.update_table() 
            self.clear_course_form()
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update course: {e}")
        finally:
            cursor.close()
            conn.close()

    
    
    def search_records(self):
        """
        Searches for records based on the query entered by the user and the selected filter.
    
        This method queries the database for matching student, instructor, or course records based on the search input 
        and the filter selected (by name, ID, or course). The results are displayed in the table.
    
        Operations:
            - If "Search by Name" is selected, searches for students, instructors, and courses by name.
            - If "Search by ID" is selected, searches for students, instructors, and courses by their ID.
            - If "Search by Course" is selected, searches for courses by course name.
    
        Error Handling:
            - If the database connection fails, the search operation is aborted.
        """
        query = self.search_input.text().lower()
        filter_by = self.search_combobox.currentText()
        self.table_widget.setRowCount(0)
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        if filter_by == "Search by Name":
            cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE %s", ('%' + query + '%',))
            for student in cursor.fetchall():
                self.insert_to_table(student, "Student")
    
            cursor.execute("SELECT * FROM instructors WHERE LOWER(name) LIKE %s", ('%' + query + '%',))
            for instructor in cursor.fetchall():
                self.insert_to_table(instructor, "Instructor")
    
            cursor.execute("SELECT * FROM courses WHERE LOWER(course_name) LIKE %s", ('%' + query + '%',))
            for course in cursor.fetchall():
                self.insert_to_table(course, "Course")
    
        elif filter_by == "Search by ID":
            cursor.execute("SELECT * FROM students WHERE LOWER(student_id) LIKE %s", ('%' + query + '%',))
            for student in cursor.fetchall():
                self.insert_to_table(student, "Student")
    
            cursor.execute("SELECT * FROM instructors WHERE LOWER(instructor_id) LIKE %s", ('%' + query + '%',))
            for instructor in cursor.fetchall():
                self.insert_to_table(instructor, "Instructor")
    
            cursor.execute("SELECT * FROM courses WHERE LOWER(course_id) LIKE %s", ('%' + query + '%',))
            for course in cursor.fetchall():
                self.insert_to_table(course, "Course")
    
        elif filter_by == "Search by Course":
            cursor.execute("SELECT * FROM courses WHERE LOWER(course_name) LIKE %s", ('%' + query + '%',))
            for course in cursor.fetchall():
                self.insert_to_table(course, "Course")
    
        cursor.close()
        conn.close()
    
    def insert_to_table(self, entity, entity_type):
        """
        Inserts a record into the table based on the entity type (Student, Instructor, or Course).
    
        This method takes the entity data and adds it to the appropriate row in the table, displaying the relevant 
        information (name, ID, age, etc.) based on whether the entity is a student, instructor, or course.
    
        Arguments:
            entity (tuple): The record data to be displayed.
            entity_type (str): The type of the entity ("Student", "Instructor", or "Course").
        """
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
    
        if entity_type == "Student":
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(entity[1]))  # Student name
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(entity_type))  # Entity type
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(entity[0]))  # Student ID
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(entity[2])))  # Student age
        elif entity_type == "Instructor":
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(entity[1]))  # Instructor name
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(entity_type))  # Entity type
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(entity[0]))  # Instructor ID
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(entity[2])))  # Instructor age
        elif entity_type == "Course":
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(entity[1]))  # Course name
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(entity_type))  # Entity type
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(entity[0]))  # Course ID
            self.table_widget.setItem(row_position, 3, QTableWidgetItem("N/A"))  # Age: N/A for courses
    
    def edit_student(self, selected_row):
        """
        Loads the selected student's data into the input fields for editing.
    
        This method retrieves the student ID from the selected row, queries the database for the student record,
        and populates the student input fields with the retrieved data. It also adds an "Update Student" button 
        to save changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the student data cannot be loaded from the database.
        """
        student_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
            student = cursor.fetchone()
    
            if student:
                self.student_name_input.setText(student[1])
                self.student_age_input.setText(str(student[2]))
                self.student_email_input.setText(student[3])
                self.student_id_input.setText(student[0])
    
                self.update_button = QPushButton("Update Student")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_student, student_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def edit_instructor(self, selected_row):
        """
        Loads the selected instructor's data into the input fields for editing.
    
        This method retrieves the instructor ID from the selected row, queries the database for the instructor record,
        and populates the instructor input fields with the retrieved data. It also adds an "Update Instructor" button 
        to save changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the instructor data cannot be loaded from the database.
        """
        instructor_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM instructors WHERE instructor_id = %s', (instructor_id,))
            instructor = cursor.fetchone()
    
            if instructor:
                self.instructor_name_input.setText(instructor[1])
                self.instructor_age_input.setText(str(instructor[2]))
                self.instructor_email_input.setText(instructor[3])
                self.instructor_id_input.setText(instructor[0])
    
                self.update_button = QPushButton("Update Instructor")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_instructor, instructor_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load instructor: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def edit_course(self, selected_row):
        """
        Loads the selected course's data into the input fields for editing.
    
        This method retrieves the course ID from the selected row, queries the database for the course record,
        and populates the course input fields with the retrieved data. It also adds an "Update Course" button 
        to save changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the course data cannot be loaded from the database.
        """
        course_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
            course = cursor.fetchone()
    
            if course:
                self.course_name_input.setText(course[1])
                self.course_id_input.setText(course[0])
    
                self.update_button = QPushButton("Update Course")
                self.update_button.setStyleSheet("background-color: #ffeb3b; color: black;")
                self.update_button.clicked.connect(partial(self.update_course, course_id))
                self.left_layout.addWidget(self.update_button)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load course: {e}")
        finally:
            cursor.close()
            conn.close()

    
    def delete_student(self, selected_row):
        """
        Deletes the selected student from the database.
    
        This method retrieves the student ID from the selected row in the table, deletes the corresponding 
        student record from the database, and updates the table to reflect the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the student deletion fails.
        """
        student_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Student deleted successfully!")
            self.update_table() 
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete student: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def delete_instructor(self, selected_row):
        """
        Deletes the selected instructor from the database.
    
        This method retrieves the instructor ID from the selected row in the table, deletes the corresponding 
        instructor record from the database, and updates the table to reflect the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the instructor deletion fails.
        """
        instructor_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('DELETE FROM instructors WHERE instructor_id = %s', (instructor_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Instructor deleted successfully!")
            self.update_table()
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete instructor: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def delete_course(self, selected_row):
        """
        Deletes the selected course from the database.
    
        This method retrieves the course ID from the selected row in the table, deletes the corresponding 
        course record from the database, and updates the table to reflect the changes.
    
        Arguments:
            selected_row (int): The index of the selected row in the table.
    
        Error Handling:
            - Displays an error message if the course deletion fails.
        """
        course_id = self.table_widget.item(selected_row, 2).text()
    
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()
    
        try:
            cursor.execute('DELETE FROM courses WHERE course_id = %s', (course_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Course deleted successfully!")
            self.update_table()
    
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete course: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def clear_student_form(self):
        """
        Clears the input fields for student data.
    
        This method resets the student form by clearing the student name, age, email, and ID input fields.
        """
        self.student_name_input.clear()
        self.student_age_input.clear()
        self.student_email_input.clear() 
        self.student_id_input.clear()
    
    def clear_instructor_form(self):
        """
        Clears the input fields for instructor data.
    
        This method resets the instructor form by clearing the instructor name, age, email, and ID input fields.
        """
        self.instructor_name_input.clear()
        self.instructor_age_input.clear()
        self.instructor_email_input.clear() 
        self.instructor_id_input.clear()
    
    def clear_course_form(self):
        """
        Clears the input fields for course data.
    
        This method resets the course form by clearing the course ID and course name input fields.
        """
        self.course_id_input.clear()
        self.course_name_input.clear()
    
    def add_export_button(self):
        """
        Adds an "Export to CSV" button to the GUI.
    
        This method creates an export button, styles it, and connects it to the `export_to_csv()` method.
        """
        export_button = QPushButton("Export to CSV")
    
        export_button.setStyleSheet("""
            background-color: #ff9800;
            color: white;
            font-weight: bold;
            padding: 10px 15px;
            border-radius: 5px;
        """)
    
        export_button.clicked.connect(self.export_to_csv)
    
        self.left_layout.addWidget(export_button)
    
    def export_to_csv(self):
        """
        Exports the system data (students, instructors, and courses) to a CSV file.
    
        This method opens a file dialog for the user to select a file location, retrieves the data from the database, 
        and writes it to a CSV file.
    
        Error Handling:
            - Displays an error message if the data export fails.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv)", options=options)
    
        if file_path:
            conn = connect_to_db()
            if not conn:
                return
            cursor = conn.cursor()
    
            try:
                data = []
    
                cursor.execute("SELECT * FROM students")
                for student in cursor.fetchall():
                    data.append([student[1], "Student", student[0], student[2], student[3]])  
    
                cursor.execute("SELECT * FROM instructors")
                for instructor in cursor.fetchall():
                    data.append([instructor[1], "Instructor", instructor[0], instructor[2], instructor[3]]) 
    
                cursor.execute("SELECT * FROM courses")
                for course in cursor.fetchall():
                    data.append([course[1], "Course", course[0], "N/A", "N/A"]) 
    
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Name", "Type", "ID", "Age", "Email"])
                    writer.writerows(data)
    
                QMessageBox.information(self, "Success", "Data exported to CSV successfully.")
    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {e}")
    
            finally:
                cursor.close()
                conn.close()
    
    def backup_database(self):
        """
        Backs up the database to a JSON file.
    
        This method opens a file dialog for the user to select a file location, retrieves all data (students, instructors, 
        courses, registrations, and course assignments) from the database, and writes the backup to a JSON file.
    
        Error Handling:
            - Displays an error message if the database backup fails.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Backup Database", "", "JSON Files (*.json)", options=options)
    
        if file_path:
            conn = connect_to_db()
            if not conn:
                return
            cursor = conn.cursor()
    
            try:
                # Fetch data from all tables
                cursor.execute("SELECT * FROM students")
                students = cursor.fetchall()
    
                cursor.execute("SELECT * FROM instructors")
                instructors = cursor.fetchall()
    
                cursor.execute("SELECT * FROM courses")
                courses = cursor.fetchall()
    
                cursor.execute("SELECT * FROM registrations")
                registrations = cursor.fetchall()
    
                cursor.execute("SELECT * FROM course_assignments")
                assignments = cursor.fetchall()
    
                backup_data = {
                    "students": [{"student_id": s[0], "name": s[1], "age": s[2], "email": s[3]} for s in students],
                    "instructors": [{"instructor_id": i[0], "name": i[1], "age": i[2], "email": i[3]} for i in instructors],
                    "courses": [{"course_id": c[0], "course_name": c[1]} for c in courses],
                    "registrations": [{"student_id": r[1], "course_id": r[2]} for r in registrations],
                    "assignments": [{"instructor_id": a[1], "course_id": a[2]} for a in assignments]
                }
    
                with open(file_path, 'w') as backup_file:
                    json.dump(backup_data, backup_file, indent=4)
                
                QMessageBox.information(self, "Success", "Database backup saved successfully!")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to back up database: {e}")
            finally:
                cursor.close()
                conn.close()
    

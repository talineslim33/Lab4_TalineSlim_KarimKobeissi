import tkinter as tk
from tkinter import ttk
import psycopg2
import json

# Database connection
conn = psycopg2.connect(
    database="School_Management_System", user='postgres',
    password='2003', host='localhost', port='5432'
)
"""
Establishes a connection to the PostgreSQL database.

:param database: The name of the database.
:type database: str
:param user: The PostgreSQL user.
:type user: str
:param password: The user's password for accessing the database.
:type password: str
:param host: The database host, typically 'localhost'.
:type host: str
:param port: The port number to access the PostgreSQL service.
:type port: int
:ivar conn: A connection object used to interact with the PostgreSQL database.
:vartype conn: psycopg2.extensions.connection
"""

cur = conn.cursor()
"""
Creates a cursor object to execute SQL commands in the PostgreSQL database.

:ivar cur: A cursor object that interacts with the database.
:vartype cur: psycopg2.extensions.cursor
"""

# Create tables if they don't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
""")
"""
Ensures the `students` table exists in the database with the following columns:
- **student_id**: Primary key, a unique identifier for each student.
- **name**: The name of the student.
- **age**: The age of the student.
- **email**: The email of the student, must be unique.
"""

cur.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        instructor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
""")
"""
Ensures the `instructors` table exists in the database with the following columns:
- **instructor_id**: Primary key, a unique identifier for each instructor.
- **name**: The name of the instructor.
- **age**: The age of the instructor.
- **email**: The email of the instructor, must be unique.
"""

cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id VARCHAR(50) PRIMARY KEY,
        course_name VARCHAR(100) NOT NULL
    );
""")
"""
Ensures the `courses` table exists in the database with the following columns:
- **course_id**: Primary key, a unique identifier for each course.
- **course_name**: The name of the course.
"""

cur.execute("""
    CREATE TABLE IF NOT EXISTS course_enrollment (
        student_id VARCHAR(50),
        course_id VARCHAR(50),
        PRIMARY KEY(student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    );
""")
"""
Ensures the `course_enrollment` table exists in the database with the following columns:
- **student_id**: Foreign key referencing the `students` table.
- **course_id**: Foreign key referencing the `courses` table.
The primary key is a combination of `student_id` and `course_id`, representing the enrollment.
"""

cur.execute("""
    CREATE TABLE IF NOT EXISTS course_instructors (
        course_id VARCHAR(50),
        instructor_id VARCHAR(50),
        PRIMARY KEY(course_id, instructor_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
        FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE
    );
""")
"""
Ensures the `course_instructors` table exists in the database with the following columns:
- **course_id**: Foreign key referencing the `courses` table.
- **instructor_id**: Foreign key referencing the `instructors` table.
The primary key is a combination of `course_id` and `instructor_id`, representing course assignments.
"""

conn.commit()
"""
Commits the executed SQL queries to the database to save changes.
"""

# Create main window
root = tk.Tk()
"""
Initializes the main Tkinter window for the School Management System application.
"""

root.title("School Management System")
root.geometry("1200x700")
root.config(bg="#2F3E46")
"""
Configures the Tkinter window with a title, size, and background color.

:ivar root: The root window of the Tkinter application.
:vartype root: tkinter.Tk
"""

# Custom Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Helvetica", 12), background="#2F3E46", foreground="white")
style.configure("TButton", font=("Helvetica", 12), background="#3A506B", foreground="white")
style.configure("TEntry", font=("Helvetica", 12), background="#CAD2C5")
style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#3A506B", foreground="white")
"""
Sets up custom styles for Tkinter widgets, including labels, buttons, entries, and treeviews.
"""

def add_student():
    """
    Adds a new student record to the `students` table in the PostgreSQL database.

    Retrieves input from the Tkinter entry fields and inserts a new student record.
    After successfully adding the student to the database, it updates the displayed
    records and clears the input fields.

    :raises psycopg2.Error: If an error occurs during the database operation.
    :return: None
    """
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    student_id = student_id_entry.get()

    if name and age and email and student_id:
        try:
            cur.execute(
                "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (student_id, name, int(age), email)
            )
            conn.commit()
            print(f"Student {name} added to the database.")
            display_all_records()

            # Update comboboxes with the new student
            update_comboboxes()

            # Clear input fields
            student_name_entry.delete(0, tk.END)
            student_age_entry.delete(0, tk.END)
            student_email_entry.delete(0, tk.END)
            student_id_entry.delete(0, tk.END)
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()

def add_instructor():
    """
    Adds a new instructor record to the `instructors` table in the PostgreSQL database.

    This function retrieves input from the Tkinter entry fields and inserts a new
    instructor record into the database. After successfully adding the instructor, it updates
    the displayed records, clears the input fields, and updates relevant comboboxes.

    :raises psycopg2.Error: If an error occurs during the database operation.
    :return: None
    """
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    if name and age and email and instructor_id:
        try:
            cur.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (instructor_id, name, int(age), email)
            )
            conn.commit()
            print(f"Instructor {name} added to the database.")
            display_all_records()

            # Update comboboxes with the new instructor
            update_comboboxes()

            # Clear input fields
            instructor_name_entry.delete(0, tk.END)
            instructor_age_entry.delete(0, tk.END)
            instructor_email_entry.delete(0, tk.END)
            instructor_id_entry.delete(0, tk.END)
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()

def add_course():
    """
    Adds a new course record to the `courses` table in the PostgreSQL database.

    This function retrieves input from the Tkinter entry fields and inserts a new
    course record into the database. After successfully adding the course, it updates
    the displayed records, clears the input fields, and updates relevant comboboxes.

    :raises psycopg2.Error: If an error occurs during the database operation.
    :return: None
    """
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()

    if course_id and course_name:
        try:
            cur.execute(
                "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)",
                (course_id, course_name)
            )
            conn.commit()
            print(f"Course {course_name} added to the database.")
            display_all_records()

            # Update comboboxes with the new course
            update_comboboxes()

            # Clear input fields
            course_id_entry.delete(0, tk.END)
            course_name_entry.delete(0, tk.END)
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def display_all_records():
    """
    Fetches and displays all records (students, instructors, courses) from the database
    and updates the Treeview widgets (tree and course_tree) with the corresponding data.

    This function clears any existing records from both Treeviews before fetching fresh data.
    Students, instructors, and courses are displayed in the main Treeview, while courses
    and their details (instructor and enrolled students) are displayed in the course_tree.

    :return: None
    """
    # Clear existing records in the main Treeview (tree)
    for item in tree.get_children():
        tree.delete(item)

    # Clear existing records in the course details Treeview (course_tree)
    for item in course_tree.get_children():
        course_tree.delete(item)

    # Fetch and display students
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    for student in students:
        tree.insert("", "end", values=(student[1], "Student", student[0], student[3]))

    # Fetch and display instructors
    cur.execute("SELECT * FROM instructors")
    instructors = cur.fetchall()
    for instructor in instructors:
        tree.insert("", "end", values=(instructor[1], "Instructor", instructor[0], instructor[3]))

    # Fetch and display courses
    cur.execute("""
        SELECT c.course_id, c.course_name, COALESCE(i.name, 'No Instructor'), 
        COALESCE(array_agg(s.name), ARRAY['None'])
        FROM courses c
        LEFT JOIN course_instructors ci ON c.course_id = ci.course_id
        LEFT JOIN instructors i ON ci.instructor_id = i.instructor_id
        LEFT JOIN course_enrollment ce ON c.course_id = ce.course_id
        LEFT JOIN students s ON ce.student_id = s.student_id
        GROUP BY c.course_id, i.name
    """)
    courses = cur.fetchall()

    # Insert data into the main tree view and the course details Treeview
    for course in courses:
        students = ', '.join([student for student in course[3] if student]) or "None"
        instructor = course[2] if course[2] else "No Instructor"

        # Insert into the main tree
        tree.insert("", "end", values=(course[1], "Course", course[0], ""))

        # Insert into the course details tree
        course_tree.insert("", "end", values=(course[1], instructor, students))


def register_student_for_course():
    """
    Registers a student for a selected course in the `course_enrollment` table.

    This function retrieves the student's ID based on their name, as well as the course ID based
    on the course name. If both IDs are valid, the student is registered for the course in the database.

    :raises psycopg2.Error: If an error occurs during the database operation.
    :return: None
    """
    student_name = student_combobox.get()
    selected_course_name = course_combobox.get()

    cur.execute("SELECT student_id FROM students WHERE name = %s", (student_name,))
    student_id = cur.fetchone()

    cur.execute("SELECT course_id FROM courses WHERE course_name = %s", (selected_course_name,))
    course_id = cur.fetchone()

    if student_id and course_id:
        try:
            cur.execute(
                "INSERT INTO course_enrollment (student_id, course_id) VALUES (%s, %s)",
                (student_id[0], course_id[0])
            )
            conn.commit()
            print(f"Student {student_name} registered for {selected_course_name}.")
            display_all_records()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def assign_instructor_to_course():
    """
    Assigns an instructor to a course in the `course_instructors` table.

    This function retrieves the instructor's ID based on their name and the course ID based on
    the course name. If both IDs are valid, the instructor is assigned to the course in the database.

    :raises psycopg2.Error: If an error occurs during the database operation.
    :return: None
    """
    instructor_name = instructor_combobox.get()
    selected_course_name = instructor_course_combobox.get()

    cur.execute("SELECT instructor_id FROM instructors WHERE name = %s", (instructor_name,))
    instructor_id = cur.fetchone()

    cur.execute("SELECT course_id FROM courses WHERE course_name = %s", (selected_course_name,))
    course_id = cur.fetchone()

    if instructor_id and course_id:
        try:
            cur.execute(
                "INSERT INTO course_instructors (instructor_id, course_id) VALUES (%s, %s)",
                (instructor_id[0], course_id[0])
            )
            conn.commit()
            print(f"Instructor {instructor_name} assigned to {selected_course_name}.")
            display_all_records()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def delete_record():
    """
    Deletes a selected record (student, instructor, or course) from the database.

    The function checks the type of the selected record from the Treeview and deletes
    the corresponding record from the database. The display is updated after the deletion.

    :raises psycopg2.Error: If an error occurs during the deletion operation.
    :return: None
    """
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        record_type = values[1]

        if record_type == "Student":
            try:
                cur.execute("DELETE FROM students WHERE student_id = %s", (values[2],))
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error: {e}")
                conn.rollback()

        elif record_type == "Instructor":
            try:
                cur.execute("DELETE FROM instructors WHERE instructor_id = %s", (values[2],))
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error: {e}")
                conn.rollback()

        elif record_type == "Course":
            try:
                cur.execute("DELETE FROM courses WHERE course_id = %s", (values[2],))
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error: {e}")
                conn.rollback()

        display_all_records()


def search_records():
    """
    Searches for records (students, instructors, or courses) based on the query and search type.

    This function allows searching by either name or ID. The query is case-insensitive.
    The Treeview is updated with the search results after fetching records from the database.

    :return: None
    """
    query = search_entry.get().lower()
    search_type = search_type_combobox.get().lower()

    # Clear existing records from the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Search by name
    if search_type == "name":
        cur.execute("SELECT * FROM students WHERE LOWER(name) LIKE %s", (f"%{query}%",))
        students = cur.fetchall()
        for student in students:
            tree.insert("", "end", values=(student[1], "Student", student[0], student[3]))

        cur.execute("SELECT * FROM instructors WHERE LOWER(name) LIKE %s", (f"%{query}%",))
        instructors = cur.fetchall()
        for instructor in instructors:
            tree.insert("", "end", values=(instructor[1], "Instructor", instructor[0], instructor[3]))

        cur.execute("SELECT * FROM courses WHERE LOWER(course_name) LIKE %s", (f"%{query}%",))
        courses = cur.fetchall()
        for course in courses:
            tree.insert("", "end", values=(course[1], "Course", course[0], ""))

    # Search by ID
    elif search_type == "id":
        cur.execute("SELECT * FROM students WHERE student_id LIKE %s", (f"%{query}%",))
        students = cur.fetchall()
        for student in students:
            tree.insert("", "end", values=(student[1], "Student", student[0], student[3]))

        cur.execute("SELECT * FROM instructors WHERE instructor_id LIKE %s", (f"%{query}%",))
        instructors = cur.fetchall()
        for instructor in instructors:
            tree.insert("", "end", values=(instructor[1], "Instructor", instructor[0], instructor[3]))


def update_student(student_id):
    """
    Updates the details of a student in the `students` table in the PostgreSQL database.

    This function updates the student's name, age, and email based on the provided `student_id`.
    After the update, it resets the input fields, updates the comboboxes, and refreshes the displayed records.

    :param student_id: The unique identifier of the student to be updated.
    :type student_id: str
    :raises psycopg2.Error: If an error occurs during the database update operation.
    :return: None
    """
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()

    if name and age and email:
        try:
            cur.execute(
                "UPDATE students SET name = %s, age = %s, email = %s WHERE student_id = %s",
                (name, int(age), email, student_id)
            )
            conn.commit()
            print(f"Student {name} updated in the database.")
            display_all_records()

            # Reset the button and input fields after update
            reset_buttons()

            # Refresh the comboboxes to reflect updated values
            update_comboboxes()

        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def update_comboboxes():
    """
    Updates the values in the student, instructor, and course comboboxes based on the current records in the database.

    This function retrieves the updated student, instructor, and course data from the database and updates
    the corresponding comboboxes in the UI.

    :return: None
    """
    # Fetch and update student combobox
    cur.execute("SELECT name FROM students")
    students = cur.fetchall()
    student_combobox['values'] = [student[0] for student in students]  # Populate student names

    # Fetch and update instructor combobox
    cur.execute("SELECT name FROM instructors")
    instructors = cur.fetchall()
    instructor_combobox['values'] = [instructor[0] for instructor in instructors]  # Populate instructor names

    # Fetch and update course comboboxes
    cur.execute("SELECT course_name FROM courses")
    courses = cur.fetchall()
    course_combobox['values'] = [course[0] for course in courses]
    instructor_course_combobox['values'] = [course[0] for course in courses]


def update_course(course_id):
    """
    Updates the name of a course in the `courses` table in the PostgreSQL database.

    This function updates the course name based on the provided `course_id`. After the update, it resets
    the input fields, updates the comboboxes, and refreshes the displayed records.

    :param course_id: The unique identifier of the course to be updated.
    :type course_id: str
    :raises psycopg2.Error: If an error occurs during the database update operation.
    :return: None
    """
    course_name = course_name_entry.get()

    if course_name:
        try:
            cur.execute(
                "UPDATE courses SET course_name = %s WHERE course_id = %s",
                (course_name, course_id)
            )
            conn.commit()
            print(f"Course {course_name} updated in the database.")
            display_all_records()

            # Reset the button and input fields after update
            reset_buttons()

            # Refresh the comboboxes to reflect updated values
            update_comboboxes()

        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def update_instructor(instructor_id):
    """
    Updates the details of an instructor in the `instructors` table in the PostgreSQL database.

    This function updates the instructor's name, age, and email based on the provided `instructor_id`.
    After the update, it resets the input fields, updates the comboboxes, and refreshes the displayed records.

    :param instructor_id: The unique identifier of the instructor to be updated.
    :type instructor_id: str
    :raises psycopg2.Error: If an error occurs during the database update operation.
    :return: None
    """
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()

    if name and age and email:
        try:
            cur.execute(
                "UPDATE instructors SET name = %s, age = %s, email = %s WHERE instructor_id = %s",
                (name, int(age), email, instructor_id)
            )
            conn.commit()
            print(f"Instructor {name} updated in the database.")
            display_all_records()

            # Reset the button and input fields after update
            reset_buttons()

            # Refresh the comboboxes to reflect updated values
            update_comboboxes()

        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()


def edit_record():
    """
    Loads the details of the selected record from the Treeview into the input fields for editing.

    This function retrieves the details of the selected student, instructor, or course from the Treeview.
    Based on the record type (student, instructor, or course), it updates the corresponding input fields
    and changes the "Add" button to an "Update" button.

    :return: None
    """
    selected_item = tree.selection()  # Get selected item from Treeview
    if selected_item:
        values = tree.item(selected_item, 'values')  # Get the values of the selected item
        record_type = values[1]  # Check if it's a Student, Instructor, or Course

        # If the selected record is a Student
        if record_type == "Student":
            cur.execute("SELECT * FROM students WHERE student_id = %s", (values[2],))
            student = cur.fetchone()
            if student:
                student_name_entry.delete(0, tk.END)
                student_age_entry.delete(0, tk.END)
                student_email_entry.delete(0, tk.END)
                student_id_entry.delete(0, tk.END)

                student_name_entry.insert(0, student[1])
                student_age_entry.insert(0, student[2])
                student_email_entry.insert(0, student[3])
                student_id_entry.insert(0, student[0])

                # Change Add button to Update button for Student
                tk.Button(left_frame, text="Update Student", command=lambda: update_student(student[0]), bg="#FFB74D", fg="black").grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        # If the selected record is an Instructor
        elif record_type == "Instructor":
            cur.execute("SELECT * FROM instructors WHERE instructor_id = %s", (values[2],))
            instructor = cur.fetchone()
            if instructor:
                instructor_name_entry.delete(0, tk.END)
                instructor_age_entry.delete(0, tk.END)
                instructor_email_entry.delete(0, tk.END)
                instructor_id_entry.delete(0, tk.END)

                instructor_name_entry.insert(0, instructor[1])
                instructor_age_entry.insert(0, instructor[2])
                instructor_email_entry.insert(0, instructor[3])
                instructor_id_entry.insert(0, instructor[0])

                # Change Add button to Update button for Instructor
                tk.Button(left_frame, text="Update Instructor", command=lambda: update_instructor(instructor[0]), bg="#FFB74D", fg="black").grid(row=10, column=1, sticky="ew", padx=10, pady=5)

        # If the selected record is a Course
        elif record_type == "Course":
            cur.execute("SELECT * FROM courses WHERE course_id = %s", (values[2],))
            course = cur.fetchone()
            if course:
                course_id_entry.delete(0, tk.END)
                course_name_entry.delete(0, tk.END)

                course_id_entry.insert(0, course[0])
                course_name_entry.insert(0, course[1])

                # Change Add button to Update button for Course
                tk.Button(left_frame, text="Update Course", command=lambda: update_course(course[0]), bg="#FFB74D", fg="black").grid(row=13, column=1, sticky="ew", padx=10, pady=5)


def save_data():
    """
    Fetches data from the PostgreSQL database and saves it to a JSON file.

    This function retrieves all records from the `students`, `instructors`, and `courses` tables,
    organizes the data into a dictionary, and writes the dictionary to a JSON file named `backup_data.json`.

    :return: None
    """
    # Fetch data from the database
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    
    cur.execute("SELECT * FROM instructors")
    instructors = cur.fetchall()
    
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    # Create a dictionary to hold all data
    data = {
        'students': [{'student_id': student[0], 'name': student[1], 'age': student[2], 'email': student[3]} for student in students],
        'instructors': [{'instructor_id': instructor[0], 'name': instructor[1], 'age': instructor[2], 'email': instructor[3]} for instructor in instructors],
        'courses': [{'course_id': course[0], 'course_name': course[1]} for course in courses]
    }

    # Save data to JSON file
    with open('backup_data.json', 'w') as file:
        json.dump(data, file, indent=4)

    print("Data saved to 'backup_data.json'")


def load_data():
    """
    Loads data from a JSON file and inserts it into the PostgreSQL database.

    This function reads data from the `backup_data.json` file, clears existing records from the database,
    and inserts the loaded data into the `students`, `instructors`, and `courses` tables.

    If the file is not found, an error message is printed.

    :raises FileNotFoundError: If the JSON file (`backup_data.json`) is not found.
    :return: None
    """
    # Load data from JSON file
    try:
        with open('backup_data.json', 'r') as file:
            data = json.load(file)

        # Clear existing data from the database
        cur.execute("DELETE FROM course_enrollment")
        cur.execute("DELETE FROM course_instructors")
        cur.execute("DELETE FROM students")
        cur.execute("DELETE FROM instructors")
        cur.execute("DELETE FROM courses")
        conn.commit()

        # Insert students
        for student in data['students']:
            cur.execute(
                "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (student['student_id'], student['name'], student['age'], student['email'])
            )

        # Insert instructors
        for instructor in data['instructors']:
            cur.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (instructor['instructor_id'], instructor['name'], instructor['age'], instructor['email'])
            )

        # Insert courses
        for course in data['courses']:
            cur.execute(
                "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)",
                (course['course_id'], course['course_name'])
            )

        conn.commit()
        display_all_records()
        
        # Refresh comboboxes with the loaded data
        update_comboboxes()
        
        print("Data loaded from 'backup_data.json'")
    except FileNotFoundError:
        print("File not found.")



def reset_buttons():
    """
    Resets the buttons in the UI for adding a student, instructor, or course.

    This function sets the buttons to their default state for adding new records (student, instructor, course).
    It also clears the input fields for students, instructors, and courses.

    :return: None
    """
    # Reset the button to "Add Student" for students
    tk.Button(left_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white").grid(row=5, column=1, sticky="ew", padx=10, pady=5)
    
    # Reset the button to "Add Instructor" for instructors
    tk.Button(left_frame, text="Add Instructor", command=add_instructor, bg="#4CAF50", fg="white").grid(row=10, column=1, sticky="ew", padx=10, pady=5)

    # Reset the button to "Add Course" for courses
    tk.Button(left_frame, text="Add Course", command=add_course, bg="#4CAF50", fg="white").grid(row=13, column=1, sticky="ew", padx=10, pady=5)

    # Clear input fields after the update
    student_name_entry.delete(0, tk.END)
    student_age_entry.delete(0, tk.END)
    student_email_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    instructor_name_entry.delete(0, tk.END)
    instructor_age_entry.delete(0, tk.END)
    instructor_email_entry.delete(0, tk.END)
    instructor_id_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)


# UI layout configuration
"""
Sets up the layout of the user interface, including the main frame, left and right frames,
and their widgets such as Treeview, entry fields, buttons, and comboboxes.
"""

main_frame = tk.Frame(root, bg="#2F3E46")
main_frame.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, bg="#354F52", padx=20, pady=20)
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = tk.Frame(main_frame, bg="#2F3E46")
right_frame.grid(row=0, column=1, sticky="nsew")

course_tree = ttk.Treeview(right_frame, columns=("Course Name", "Instructor", "Students"), show="headings", height=10)
course_tree.heading("Course Name", text="Course Name")
course_tree.heading("Instructor", text="Instructor")
course_tree.heading("Students", text="Students")
course_tree.grid(row=1, column=0, sticky="nsew")

# Configure the right frame grid layout
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Search Frame
"""
Configures the search frame for the UI where users can search by name, ID, or course.
Includes a search entry box and a search type combobox.
"""
search_frame = tk.Frame(left_frame, bg="#354F52", padx=20, pady=10)
search_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

tk.Label(search_frame, text="Search:", bg="#354F52", fg="white").grid(row=0, column=0, padx=10, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=10, pady=5)

search_type_combobox = ttk.Combobox(search_frame, values=["Name", "ID", "Course"], state="readonly")
search_type_combobox.grid(row=0, column=2, padx=10, pady=5)
search_type_combobox.set("Name")

tk.Button(search_frame, text="Search", command=lambda: search_records(), bg="#3A506B", fg="white").grid(row=0, column=3, padx=10, pady=5)

# Student Form
"""
Form for entering and adding student information (name, age, email, ID).
"""
tk.Label(left_frame, text="Student Name:", bg="#354F52", fg="white").grid(row=1, column=0, padx=10, pady=5)
student_name_entry = tk.Entry(left_frame)
student_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Age:", bg="#354F52", fg="white").grid(row=2, column=0, padx=10, pady=5)
student_age_entry = tk.Entry(left_frame)
student_age_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Email:", bg="#354F52", fg="white").grid(row=3, column=0, padx=10, pady=5)
student_email_entry = tk.Entry(left_frame)
student_email_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Student ID:", bg="#354F52", fg="white").grid(row=4, column=0, padx=10, pady=5)
student_id_entry = tk.Entry(left_frame)
student_id_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Add Student", command=add_student, bg="#3A506B", fg="white").grid(row=5, column=1, sticky="ew", padx=10, pady=5)

# Instructor Form
"""
Form for entering and adding instructor information (name, age, email, ID).
"""
tk.Label(left_frame, text="Instructor Name:", bg="#354F52", fg="white").grid(row=6, column=0, padx=10, pady=5)
instructor_name_entry = tk.Entry(left_frame)
instructor_name_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Age:", bg="#354F52", fg="white").grid(row=7, column=0, padx=10, pady=5)
instructor_age_entry = tk.Entry(left_frame)
instructor_age_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Email:", bg="#354F52", fg="white").grid(row=8, column=0, padx=10, pady=5)
instructor_email_entry = tk.Entry(left_frame)
instructor_email_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Instructor ID:", bg="#354F52", fg="white").grid(row=9, column=0, padx=10, pady=5)
instructor_id_entry = tk.Entry(left_frame)
instructor_id_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Add Instructor", command=add_instructor, bg="#3A506B", fg="white").grid(row=10, column=1, sticky="ew", padx=10, pady=5)

# Course Form
"""
Form for entering and adding course information (ID, name).
"""
tk.Label(left_frame, text="Course ID:", bg="#354F52", fg="white").grid(row=11, column=0, padx=10, pady=5)
course_id_entry = tk.Entry(left_frame)
course_id_entry.grid(row=11, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Course Name:", bg="#354F52", fg="white").grid(row=12, column=0, padx=10, pady=5)
course_name_entry = tk.Entry(left_frame)
course_name_entry.grid(row=12, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Add Course", command=add_course, bg="#3A506B", fg="white").grid(row=13, column=1, sticky="ew", padx=10, pady=5)

# Dropdowns for student registration and instructor assignment
"""
Dropdowns for selecting students, instructors, and courses for registration or assignment.
"""
tk.Label(left_frame, text="Select Student:", bg="#354F52", fg="white").grid(row=14, column=0, padx=10, pady=5)
student_combobox = ttk.Combobox(left_frame, values=[])
student_combobox.grid(row=14, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Select Course for Registration:", bg="#354F52", fg="white").grid(row=15, column=0, padx=10, pady=5)
course_combobox = ttk.Combobox(left_frame, values=[])
course_combobox.grid(row=15, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Register Student for Course", command=register_student_for_course, bg="#3A506B", fg="white").grid(row=16, column=1, sticky="ew", padx=10, pady=5)

tk.Label(left_frame, text="Select Instructor:", bg="#354F52", fg="white").grid(row=17, column=0, padx=10, pady=5)
instructor_combobox = ttk.Combobox(left_frame, values=[])
instructor_combobox.grid(row=17, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Select Course for Assignment:", bg="#354F52", fg="white").grid(row=18, column=0, padx=10, pady=5)
instructor_course_combobox = ttk.Combobox(left_frame, values=[])
instructor_course_combobox.grid(row=18, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Assign Instructor to Course", command=assign_instructor_to_course, bg="#3A506B", fg="white").grid(row=19, column=1, sticky="ew", padx=10, pady=5)

# Treeview for displaying records in the right frame
"""
Displays records (students, instructors, courses) in a Treeview widget on the right side of the UI.
"""
tree = ttk.Treeview(right_frame, columns=("Name", "Type", "ID", "Email"), show="headings", height=25)
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree.heading("ID", text="ID")
tree.heading("Email", text="Email")
tree.grid(row=0, column=0, sticky="nsew")

# Configure right frame grid layout
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Frame for Edit, Delete, Save, and Load buttons
"""
Frame to hold buttons for editing, deleting, saving, and loading records.
"""
button_frame = tk.Frame(left_frame, bg="#354F52")
button_frame.grid(row=20, column=0, columnspan=2, pady=10)

# Edit, Delete, Save, and Load Buttons
edit_button = tk.Button(button_frame, text="Edit", command=lambda: edit_record(), bg="#FFB74D", fg="black")
edit_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete", command=lambda: delete_record(), bg="#E57373", fg="white")
delete_button.pack(side=tk.LEFT, padx=5)

# Save Button
save_button = tk.Button(button_frame, text="Save Data", command=save_data, bg="#66BB6A", fg="white")
save_button.pack(side=tk.RIGHT, padx=5)

# Load Button
load_button = tk.Button(button_frame, text="Load Data", command=load_data, bg="#42A5F5", fg="white")
load_button.pack(side=tk.RIGHT, padx=5)

# Run the application
"""
Starts the Tkinter main loop and runs the application.
"""
root.mainloop()

# Close the database connection when the app is closed
"""
Closes the PostgreSQL database connection once the application is terminated.
"""
conn.close()

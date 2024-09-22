# School Management System using Tkinter

## Overview
The *School Management System* is a desktop application developed in Python using *Tkinter* for the graphical user interface (GUI) and *PostgreSQL* for the database backend. It allows users to manage the school’s students, instructors, and courses efficiently. The system features a range of functionalities, including adding, updating, and deleting records for students, instructors, and courses. It also allows for assigning students to courses and instructors to courses, with all data securely stored in a PostgreSQL database.

The system also supports *data backup* and *restore* through *JSON files*, making it easy to manage and persist data across sessions.

## Key Features

1. *User-Friendly Interface:*
   - Designed using *Tkinter*, the system has a clear and intuitive interface.
   - Custom *styling* applied using ttk.Style for a modern and sleek look.
   
2. *Database Integration:*
   - Integrated with *PostgreSQL* for robust data handling.
   - Data persistence for students, instructors, and courses.
   - Tables include *foreign key constraints* to maintain relationships and data integrity.

3. *Add, Update, and Delete Operations:*
   - Add new students, instructors, and courses with unique IDs.
   - Update existing records with real-time updates in the interface.
   - Delete records, with foreign key constraints ensuring cascading deletions (i.e., when a student is deleted, they are also removed from the courses they were enrolled in).

4. *Student and Instructor Management:*
   - Add students and instructors with details such as name, age, and email.
   - Assign instructors to courses.
   - Register students for courses.
   
5. *Treeview Display:*
   - View all students, instructors, and courses in a *Treeview widget*.
   - Dynamic updates to reflect the current state of the database.

6. *Search Functionality:*
   - Search records by name or ID, filtering the results dynamically in the Treeview.

7. *Data Backup and Restore:*
   - Save data to a *JSON* file for backup.
   - Load data from the JSON file into the PostgreSQL database.
   
8. *Course Management:*
   - Create and manage courses.
   - Register students for specific courses.
   - Assign instructors to courses.

## Database Schema

The School Management System uses PostgreSQL for database management, with the following tables:

### 1. students
| Column        | Type         | Description                                  |
|---------------|--------------|----------------------------------------------|
| student_id  | VARCHAR(50)  | Unique identifier for each student (Primary Key) |
| name        | VARCHAR(100) | Full name of the student                     |
| age         | INT          | Age of the student                           |
| email       | VARCHAR(100) | Email address of the student (Unique)        |

### 2. instructors
| Column          | Type         | Description                                  |
|-----------------|--------------|----------------------------------------------|
| instructor_id | VARCHAR(50)  | Unique identifier for each instructor (Primary Key) |
| name          | VARCHAR(100) | Full name of the instructor                  |
| age           | INT          | Age of the instructor                        |
| email         | VARCHAR(100) | Email address of the instructor (Unique)     |

### 3. courses
| Column       | Type         | Description                                  |
|--------------|--------------|----------------------------------------------|
| course_id  | VARCHAR(50)  | Unique identifier for each course (Primary Key) |
| course_name| VARCHAR(100) | Name of the course                           |

### 4. course_enrollment
| Column       | Type         | Description                                  |
|--------------|--------------|----------------------------------------------|
| student_id | VARCHAR(50)  | Foreign key to students.student_id          |
| course_id  | VARCHAR(50)  | Foreign key to courses.course_id            |
- *Primary Key:* A combination of student_id and course_id.
- Enrolls students in courses and maintains the many-to-many relationship between students and courses.

### 5. course_instructors
| Column         | Type         | Description                                  |
|----------------|--------------|----------------------------------------------|
| course_id    | VARCHAR(50)  | Foreign key to courses.course_id            |
| instructor_id| VARCHAR(50)  | Foreign key to instructors.instructor_id    |
- *Primary Key:* A combination of course_id and instructor_id.
- Assigns instructors to courses and maintains the many-to-many relationship between instructors and courses.

## How to Run the Application

### Prerequisites
- *Python 3.x* must be installed on your system.
- Install required Python packages using pip:
  bash
  pip install tkinter psycopg2
  
- A running *PostgreSQL* instance. Set up the database and connection details as follows:
  - Database name: School_Management_System
  - Default credentials in the script are:
    - User: postgres
    - Password: 2003
    - Host: localhost
    - Port: 5432

### Setup Instructions

1. *Database Setup:*
   - Create the database in PostgreSQL using the following command:
     sql
     CREATE DATABASE School_Management_System;
     
   - Ensure the students, instructors, courses, course_enrollment, and course_instructors tables are created automatically when running the app.

2. *Running the Application:*
   - Clone the repository or copy the script to your local machine.
   - Ensure the PostgreSQL database is running and the credentials are correctly set in the script.
   - Run the script using Python:
     bash
     python your_script_name.py
     
   - The GUI will open, allowing you to manage students, instructors, and courses.

3. *Optional: Save and Load Data:*
   - Use the *Save Data* button to save the current database state to a JSON file (backup_data.json).
   - Use the *Load Data* button to load data from a previously saved JSON file.

### GUI Walkthrough

- *Left Panel:*
  - *Student, Instructor, and Course Forms:* Add new entries for students, instructors, and courses.
  - *Dropdowns for Enrollment and Assignment:* Register students for courses and assign instructors.
  - *Search Feature:* Find students, instructors, or courses using name or ID.
  
- *Right Panel:*
  - *Treeview Widgets:* Display students, instructors, and courses.
  - *Course Details View:* View courses along with assigned instructors and enrolled students.

- *Button Controls:*
  - *Edit:* Load the selected record for editing.
  - *Delete:* Remove the selected record from the database.
  - *Save Data:* Save the current state of the database to a JSON file.
  - *Load Data:* Load data from a JSON backup file.

## Error Handling
- Database operations are wrapped in *try-except blocks* to handle database-related errors such as:
  - Unique constraint violations (e.g., duplicate emails).
  - Foreign key constraint violations (e.g., deleting a student who is enrolled in a course).
- *Rollback* is used to revert changes if an error occurs during database operations.

## Technologies Used
- *Python 3.x* for the core logic and Tkinter GUI.
- *Tkinter* and *ttk* for the user interface.
- *PostgreSQL* for database management.
- *psycopg2* for interacting with the PostgreSQL database.
- *JSON* for data backup and restore functionality.

## Future Improvements
- *User Authentication:* Adding a login system to secure the application.
- *Course Scheduling:* Allow instructors to schedule courses and manage timings.
- *Export to CSV:* Add functionality to export records to CSV files.
- *More Advanced Search Options:* Allow users to search for multiple fields or use advanced filters.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute this software as per the terms of the license.


This README.md file provides an extensive overview of the project, including key features, database schema, installation instructions, error handling, and possible future improvements. You can adapt this to suit any specific requirements or features of your project.



# School Management System with PyQT

## Overview
The *School Management System* is a desktop application developed using *Python* and *PyQt5* for the graphical user interface (GUI), and *PostgreSQL* for the database backend. The system allows users to manage students, instructors, and courses, register students in courses, and assign instructors to courses. It also provides data backup and restore functionality with *JSON* and *CSV* exports.

This system is ideal for managing educational institutions' data in a user-friendly environment with features for adding, editing, deleting, and displaying records.

## Features

### Core Functionalities
1. *Student Management:*
   - Add, update, delete, and display student information (ID, name, age, email).
   - Register students for courses.

2. *Instructor Management:*
   - Add, update, delete, and display instructor information (ID, name, age, email).
   - Assign instructors to courses.

3. *Course Management:*
   - Add, update, delete, and display courses (ID, course name).

4. *Database Backup and Restore:*
   - Save and load data to/from a *PostgreSQL* database.
   - Backup and restore data to/from *JSON* files.
   - Export system data to *CSV*.

### User Interface
- Designed using *PyQt5* for an intuitive and visually appealing interface.
- *QTableWidget* for dynamic record display with options to edit and delete records.
- *Form Layouts* for adding or editing student, instructor, and course information.

### Additional Features
- *Search Functionality:* Filter records by student name, instructor name, or course ID.
- *Data Validation:* Ensures proper input formats, e.g., valid email addresses, positive integer ages.
- *Custom Styling:* Uses custom styles for buttons, labels, and widgets for a professional appearance.

## Installation

### Prerequisites
- *Python 3.x* must be installed on your system.
- Install required dependencies using pip:
  bash
  pip install PyQt5 psycopg2
  

### Database Setup
- Install and set up *PostgreSQL* on your system.
- Create a database named School Management. You can use the following command to create it:
  sql
  CREATE DATABASE "School Management";
  
- Update the connect_to_db function in the code with your PostgreSQL credentials (e.g., username, password, host).

### Running the Application
1. Clone the repository or download the project files to your local machine.
2. Run the script using Python:
   bash
   python your_script_name.py
   

## Usage

### Adding Students, Instructors, and Courses
- Fill out the respective forms to add students, instructors, or courses.
- After adding the details, click the corresponding "Add" button to insert the data into the system.

### Register Students for Courses
- Select a student and a course from the dropdown menus and click "Register" to register the student in the selected course.

### Assign Instructors to Courses
- Select an instructor and a course from the dropdown menus and click "Assign" to assign the instructor to the selected course.

### Editing and Deleting Records
- Use the "Edit" button to modify a student, instructor, or course record.
- Use the "Delete" button to remove a record from the system.

### Backup and Restore
- Use the "Backup Database" button to save the current state of the database to a JSON file.
- Use the "Load Data" button to restore data from a JSON file.

### Export to CSV
- Use the "Export to CSV" button to export all system data to a CSV file.

## Database Schema

The system uses the following tables in *PostgreSQL*:

### 1. students
| Column        | Type    | Description                    |
|---------------|---------|--------------------------------|
| student_id  | TEXT    | Unique student ID (Primary Key) |
| name        | TEXT    | Student's full name            |
| age         | INTEGER | Student's age                  |
| email       | TEXT    | Student's email address        |

### 2. instructors
| Column          | Type    | Description                      |
|-----------------|---------|----------------------------------|
| instructor_id | TEXT    | Unique instructor ID (Primary Key)|
| name          | TEXT    | Instructor's full name           |
| age           | INTEGER | Instructor's age                 |
| email         | TEXT    | Instructor's email address       |

### 3. courses
| Column       | Type    | Description                      |
|--------------|---------|----------------------------------|
| course_id  | TEXT    | Unique course ID (Primary Key)    |
| course_name| TEXT    | Name of the course               |

### 4. registrations
| Column           | Type    | Description                      |
|------------------|---------|----------------------------------|
| registration_id | SERIAL  | Registration ID (Primary Key)    |
| student_id      | TEXT    | Foreign key referencing students(student_id) |
| course_id       | TEXT    | Foreign key referencing courses(course_id)  |

### 5. course_assignments
| Column           | Type    | Description                      |
|------------------|---------|----------------------------------|
| assignment_id   | SERIAL  | Assignment ID (Primary Key)      |
| instructor_id   | TEXT    | Foreign key referencing instructors(instructor_id) |
| course_id       | TEXT    | Foreign key referencing courses(course_id) |

## Customization and Extensibility

### Adding New Features
The system is built to be extensible. Developers can add more features, such as:
- *User Authentication* for securing the application.
- *Scheduling* courses for instructors with date and time management.
- *Reporting* for generating detailed analytics on students, instructors, and courses.

## Troubleshooting

### Database Connection Issues
- Ensure that your PostgreSQL server is running and accessible.
- Verify that the database credentials in the connect_to_db function are correct.

### PyQt5 Installation Issues
- If you encounter issues installing PyQt5, ensure you are using the correct version of Python and pip.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license.


This README.md file provides detailed instructions for installing, setting up, and using the School Management System, including key features, database schema, and troubleshooting tips. You can adapt this template based on your specific project needs.




This is what combines both Tkinter and PyQT:

# School Management System

## Overview
The *School Management System* is a desktop application developed in Python that offers two different graphical user interfaces (GUIs):
1. *Tkinter GUI*
2. *PyQt5 GUI*

Both interfaces allow users to manage students, instructors, and courses, register students in courses, and assign instructors to courses. Additionally, the system supports data backup and restore functionality with *JSON* and *CSV* exports.

### Key Features (in Both GUIs)
- *Add, edit, and delete records* for students, instructors, and courses.
- *Register students* to courses and *assign instructors* to courses.
- *Search functionality* to filter records by name, ID, or course.
- *Backup and restore* data using *JSON* files.
- *Export system data* to *CSV* format.

## Installation

### Prerequisites
- *Python 3.x* must be installed on your system.
- Install required dependencies using pip:
  bash
  pip install PyQt5 psycopg2
  

### Database Setup
- Install and set up *PostgreSQL* on your system.
- Create a database named School Management. You can use the following command to create it:
  sql
  CREATE DATABASE "School Management";
  
- Update the connect_to_db function in the code with your PostgreSQL credentials (e.g., username, password, host).

### Running the Application
1. Clone the repository or download the project files to your local machine.

2. To run the *Tkinter* version:
   bash
   python Tkinter_with_database.py
   

3. To run the *PyQt5* version:
   bash
   python PyQt_with_database.py
   

## Tkinter Interface

### Usage

- *Main Window*: The Tkinter interface contains a simple, user-friendly main window where you can add, edit, delete, and manage records for students, instructors, and courses.
  
- *Adding Students, Instructors, and Courses*:
  - Input the relevant data in the provided fields and click the corresponding "Add" button to save the record to the database.
  
- *Registering Students for Courses*:
  - Select a student and a course from the dropdown menus, then click the "Register" button to register the student in the course.
  
- *Assigning Instructors to Courses*:
  - Select an instructor and a course from the dropdown menus, then click the "Assign" button to assign the instructor to the course.
  
- *Editing and Deleting Records*:
  - Select a record from the list, then use the "Edit" or "Delete" buttons to modify or remove the record from the database.

- *Backup and Restore*:
  - You can back up your current data to a JSON file or restore data from a previously saved JSON file.
  
- *Export to CSV*:
  - Use the "Export to CSV" button to export all records into a CSV file.

### Interface Elements
- The interface uses standard Tkinter widgets, such as buttons, labels, and entry fields, with a straightforward design to manage the database easily.
  
## PyQt5 Interface

### Usage

- *Main Window*: The PyQt5 interface features a modern, professional layout. The left pane contains forms for adding students, instructors, and courses, while the right pane displays all records in a table.

- *Adding Students, Instructors, and Courses*:
  - Fill out the forms on the left side to add new records for students, instructors, or courses. Click the respective "Add" button to save the record to the database.

- *Registering Students for Courses*:
  - Select a student and course from the dropdown menus, then click the "Register" button to register the student for the course.

- *Assigning Instructors to Courses*:
  - Select an instructor and a course from the dropdown menus, then click the "Assign" button to assign the instructor to the course.

- *Editing and Deleting Records*:
  - In the right pane, you can find "Edit" and "Delete" buttons next to each record. Use these buttons to modify or remove a record.

- *Backup and Restore*:
  - Save the database to a JSON file using the "Backup Database" button, or restore it using the "Load Data" button.

- *Export to CSV*:
  - Use the "Export to CSV" button to save the current data in CSV format.

### Interface Elements
- The PyQt5 version offers additional styling and layout options, including dynamic tables and well-styled buttons.
- The *QTableWidget* is used for displaying records in a table format, making it easier to view and manage large datasets.

## Comparison of Tkinter and PyQt5 Interfaces

| Feature                         | Tkinter                          | PyQt5                            |
|----------------------------------|----------------------------------|----------------------------------|
| *Look and Feel*                | Simple, basic interface          | Modern, professional interface   |
| *Table View*                   | Basic Listbox                    | Dynamic QTableWidget             |
| *Form Layout*                  | Vertical arrangement             | Split panes for forms and table  |
| *Search Functionality*         | Limited to text fields           | Dropdown filters and search box  |
| *Custom Styling*               | Basic widget styling             | Advanced styling with stylesheets|
| *Data Handling*                | Same functionalities             | Same functionalities             |

## Database Schema

The system uses the following tables in *PostgreSQL*:

### 1. students
| Column        | Type    | Description                    |
|---------------|---------|--------------------------------|
| student_id  | TEXT    | Unique student ID (Primary Key) |
| name        | TEXT    | Student's full name            |
| age         | INTEGER | Student's age                  |
| email       | TEXT    | Student's email address        |

### 2. instructors
| Column          | Type    | Description                      |
|-----------------|---------|----------------------------------|
| instructor_id | TEXT    | Unique instructor ID (Primary Key)|
| name          | TEXT    | Instructor's full name           |
| age           | INTEGER | Instructor's age                 |
| email         | TEXT    | Instructor's email address       |

### 3. courses
| Column       | Type    | Description                      |
|--------------|---------|----------------------------------|
| course_id  | TEXT    | Unique course ID (Primary Key)    |
| course_name| TEXT    | Name of the course               |

### 4. registrations
| Column           | Type    | Description                      |
|------------------|---------|----------------------------------|
| registration_id | SERIAL  | Registration ID (Primary Key)    |
| student_id      | TEXT    | Foreign key referencing students(student_id) |
| course_id       | TEXT    | Foreign key referencing courses(course_id)  |

### 5. course_assignments
| Column           | Type    | Description                      |
|------------------|---------|----------------------------------|
| assignment_id   | SERIAL  | Assignment ID (Primary Key)      |
| instructor_id   | TEXT    | Foreign key referencing instructors(instructor_id) |
| course_id       | TEXT    | Foreign key referencing courses(course_id) |

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license.


### Explanation of Changes:

1. How to Run Tkinter and PyQt Interfaces:
   - Detailed instructions have been added to explain how to run both the Tkinter and PyQt5 versions separately.
   
2. Usage Instructions for Both Interfaces:
   - Specific sections have been added to guide users on how to operate the key features of the system using either Tkinter or PyQt5.

3. Comparison Table:
   - A comparison between the two GUIs has been included to highlight the key differences in look, feel, and functionality.

These additions help users understand how to interact with the two different GUIs and provide clarity on the key features for each version of the application.

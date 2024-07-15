Student Information Management System

Project Description : This project is a Student Information Management System developed for Sichuan University. It is designed to manage student data, including course registration, accommodation details, book purchases, and personal information updates. The system uses Python for the main programming logic and SQLite for database management.

Features
Student Course Registration
Student Accommodation Information Management
Student Book Purchases
Student Information Registration and Update
Data Analysis and Reporting

Technology Stack
Python: Primary programming language.
SQLite: Lightweight database for managing student information.
SQL: Database query language.
Pandas: Data analysis.
Matplotlib/Seaborn: Data visualization.

Project Structure
student-info-system/
│
├── db/
│   └── student_info_system.db  # SQLite database file
│
├── modules/
│   ├── database.py             # Database operation related code
│   ├── analysis.py             # Data analysis related code
│
└── main.py                     # Main program entry

Requirements
Database Setup 
Initialize Database: Create and initialize the database using SQLite.
Create Tables: Tables include student information, course information, course schedules, student advisor details, etc.

Data Operations 
CRUD Operations: Add new students, update student information, delete student records, query student information.
Data Insertion and Testing: Generate sample data, insert into the database, and generate a test report.
Functionality Implementation: Implement functionalities such as course registration, accommodation management, book purchases, and information updates.

Data Analysis and Reporting 
Analysis: Use Pandas or SQL to perform data analysis.
Calculate the number of students and gender ratio for each major.
Compare results across different majors.
Analyze the relationship between student age and test scores.
Analyze the relationship between students' regional distribution and test scores.
Other analyses as needed.
Reporting: Generate and display analysis reports as text output or charts.

Bonus 
GUI: Build a graphical user interface to visualize results.
DB Test Code: Write test code for the database.
Concurrent Query Tests: Perform concurrent query tests.

Getting Started
Prerequisites
Python 3.x
SQLite

Usage
Register a New Student: Add student details such as ID, name, enrollment year, major, and gender.
Course Registration: Enroll students in courses based on their major.
Book Purchase: Manage book purchases for students.
Update Information: Update student information as needed.
View/Update Grades: View and update student grades.

Example
# Add a new student
add_student_info(1, "John Doe", 2022, "Computer Science", "Male")

# Register student for a course
register_into_course(1, 101)

# Purchase a book for the student
add_book_to_student(1, 201)

# Update student information
update_student_info(1, name="John Smith")

# Fetch student information
student_info = fetch_student_info(1)
print(student_info)

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

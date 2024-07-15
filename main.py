import sqlite3
import random
from pprint import pprint

from debugpy import connect
import analysis as analysis

#conection
connection = sqlite3.connect('student_info_system.db')
cursor = connection.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Students (
#         StudentID INT PRIMARY KEY,
#         Name TEXT,
#         EnrollmentYear INT,
#         Major TEXT,
#         Gender TEXT
#     )
# ''')
# cursor.execute('''
#     alter table Students
#     add OwnedBook TEXT
#     ''')

# # Create Grades table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Grades (
#         StudentID INT,
#         CourseID INT,
#         Grade TEXT,
#         PRIMARY KEY (StudentID, CourseID),
#         FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
#         FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
#     )
# ''')

# # Create other tables
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Courses (
#         CourseID INT PRIMARY KEY,
#         CourseName TEXT,
#         Major TEXT,
#         TeacherID INT,
#         FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Teachers (
#         TeacherID INT PRIMARY KEY,
#         FirstName TEXT,
#         LastName TEXT,
#         Email TEXT
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS StudentCourses (
#         StudentID INT,
#         CourseID INT,
#         PRIMARY KEY (StudentID, CourseID),
#         FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
#         FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Books (
#         BookID INT PRIMARY KEY,
#         Title TEXT,
#         Price INT
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS CourseBooks (
#         CourseID INT,
#         BookID INT,
#         PRIMARY KEY (CourseID, BookID),
#         FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
#         FOREIGN KEY (BookID) REFERENCES Books(BookID)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS StudentCredits (
#         StudentID INT PRIMARY KEY,
#         Credit INT,
#         FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
#     )
# ''')


def fetch_all_courses_of_major(major):
    try:
        cursor.execute('''
        SELECT CourseID, CourseName FROM Courses
        WHERE Major = ?
        ''', (major,))
        return cursor.fetchall()
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return []

def register_into_course(stud_id, course_id):
    try:
        cursor.execute('''
        INSERT INTO StudentCourses (StudentID, CourseID) VALUES (?, ?)
        ''', (stud_id, course_id))
        connection.commit()
        print(f"Success! Student {stud_id} has been registered in course {course_id}.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def show_books():
    try:
        cursor.execute('''
        SELECT BookID, Title, Price FROM Books
        ''')
        return cursor.fetchall()
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return []

def add_student_info(id, name, enrol_year, major, gender):
    try:
        cursor.execute('''
        INSERT INTO Students (StudentID, Name, EnrollmentYear, Major, Gender) VALUES (?, ?, ?, ?, ?)
        ''', (id, name, enrol_year, major, gender))
        cursor.execute('''
        INSERT INTO StudentCredits (StudentID) VALUES (?)
        ''', (id,))
        connection.commit()
        print(f"Student record created successfully for {name} (ID: {id}).")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def update_student_info(id, name=None, enrol_year=None, major=None, gender=None):
    try:
        query = 'UPDATE Students SET '
        parameters = []
        if name:
            query += 'Name = ?, '
            parameters.append(name)
        if enrol_year:
            query += 'EnrollmentYear = ?, '
            parameters.append(enrol_year)
        if major:
            query += 'Major = ?, '
            parameters.append(major)
        if gender:
            query += 'Gender = ?, '
            parameters.append(gender)
        query = query.rstrip(', ')
        query += ' WHERE StudentID = ?'
        parameters.append(id)
        cursor.execute(query, parameters)
        connection.commit()
        print(f"Student information updated successfully for ID: {id}.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def delete_student(id):
    try:
        cursor.execute('''
        DELETE FROM Students WHERE StudentID = ?
        ''', (id,))
        cursor.execute('''
        DELETE FROM StudentCredits WHERE StudentID = ?
        ''', (id,))
        connection.commit()
        print(f"Student record with ID: {id} has been removed from the system.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def fetch_student_info(id):
    try:
        cursor.execute('''
        SELECT StudentID, Name, EnrollmentYear, Major, Gender FROM Students
        WHERE StudentID = ?
        ''', (id,))
        return cursor.fetchone()
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return None

def add_book_to_student(stud_id, book_id):
    try:
        cursor.execute('''
        SELECT Price FROM Books WHERE BookID = ?
        ''', (book_id,))
        price = cursor.fetchone()[0]
        cursor.execute('''
        SELECT Title FROM Books WHERE BookID = ?
        ''', (book_id,))
        title = cursor.fetchone()[0]
        cursor.execute('''
        UPDATE Students SET OwnedBook = ? WHERE StudentID = ?
        ''', (title, stud_id))
        cursor.execute('''
        UPDATE StudentCredits SET Credit = Credit - ? WHERE StudentID = ?
        ''', (price, stud_id))
        connection.commit()
        print(f"The book '{title}' has been successfully added to your account, Student ID: {stud_id}.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def is_valid_student(id):
    try:
        cursor.execute('''
        SELECT CASE WHEN EXISTS (SELECT 1 FROM Students WHERE StudentID = ?) THEN 'TRUE' ELSE 'FALSE' END
        ''', (id,))
        return cursor.fetchone()[0] == 'TRUE'
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return False

def get_name(id):
    try:
        cursor.execute('''
        SELECT Name FROM Students WHERE StudentID = ?
        ''', (id,))
        return cursor.fetchone()[0]
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return None

def add_student_grade(student_id, course_id, grade):
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO Grades (StudentID, CourseID, Grade) VALUES (?, ?, ?)
        ''', (student_id, course_id, grade))
        connection.commit()
        print(f"Grade '{grade}' added successfully for Student ID: {student_id}, Course ID: {course_id}.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def update_student_grade(student_id, course_id, new_grade):
    try:
        cursor.execute('''
        UPDATE Grades SET Grade = ? WHERE StudentID = ? AND CourseID = ?
        ''', (new_grade, student_id, course_id))
        connection.commit()
        print(f"Grade updated successfully for Student ID: {student_id}, Course ID: {course_id}.")
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")

def fetch_student_grade(student_id, course_id):
    try:
        cursor.execute('''
        SELECT Grade FROM Grades WHERE StudentID = ? AND CourseID = ?
        ''', (student_id, course_id))
        return cursor.fetchone()
    except sqlite3.DatabaseError as err:
        print(f"Database error: {err}")
        return None

def main():
    global connection, cursor
    connection = sqlite3.connect('student_info_system.db')
    cursor = connection.cursor()
    
    student_id = input("Welcome to the Student Information System! Please enter your Student ID to log in:\n")
    
    if not is_valid_student(student_id):
        print("The provided ID is invalid. Please try again.")
        return

    logged_in_name = get_name(student_id)
    
    while True:
        choice = input(f"\nHello {logged_in_name}, please choose an option from the menu:\n"
                       "1. Register a new Student\n"
                       "2. Register for a course\n"
                       "3. Purchase a book\n"
                       "4. Update your information\n"
                       "5. View/Update Grades\n"
                       "6. Log out\n")
        
        if choice == '1':
            id, name, enrol_year, major, gender = input("\nEnter the new student's information in this format: ID Name EnrollmentYear Major Gender:\n").split()
            add_student_info(id, name, int(enrol_year), major, gender)

        elif choice == '2':
            major = input("\nYou can enroll in courses from the following majors: 'CS', 'Math', 'Biology', 'Physics', 'Chemistry'.\nPlease enter the major you are interested in:\n")
            courses = fetch_all_courses_of_major(major)
            if courses:
                print(f"\nCourses available in the {major} major:\n")
                for course in courses:
                    print(course)
                course_id = input("\nEnter the Course ID you wish to enroll in:\n")
                register_into_course(student_id, course_id)
            else:
                print(f"No courses found for the {major} major.")

        elif choice == '3':
            books = show_books()
            if books:
                print("\nHere are the available books:\n")
                for book in books:
                    print(book)
                book_id = input("\nEnter the ID of the book you wish to purchase:\n")
                add_book_to_student(student_id, int(book_id))
            else:
                print("No books are currently available.")

        elif choice == '4':
            student_info = fetch_student_info(student_id)
            if student_info:
                print(f"\nYour current information:\n"
                      f"Student ID: {student_info[0]}\n"
                      f"Name: {student_info[1]}\n"
                      f"Enrollment Year: {student_info[2]}\n"
                      f"Major: {student_info[3]}\n"
                      f"Gender: {student_info[4]}")
                change_field = input("\nWhich field would you like to update (Name, EnrollmentYear, Major, Gender):\n")
                new_value = input("\nEnter the new value:\n")
                if change_field.lower() == "name":
                    update_student_info(student_id, name=new_value)
                elif change_field.lower() == "enrollmentyear":
                    update_student_info(student_id, enrol_year=int(new_value))  
                elif change_field.lower() == "major":
                    update_student_info(student_id, major=new_value)
                elif change_field.lower() == "gender":
                    update_student_info(student_id, gender=new_value)
                else:
                    print("Invalid field. Please enter a valid field name.")
            else:
                print(f"Could not retrieve information for Student ID {student_id}.")

        elif choice == '5':
            sub_choice = input("\nChoose an option:\n"
                               "1. View Grades\n"
                               "2. Update Grade\n")
            if sub_choice == '1':
                major = input("\nYou can view grades for courses from the following majors: 'CS', 'Math', 'Biology'.\nPlease enter the major you want to view grades for:\n")
                courses = fetch_all_courses_of_major(major)
                if courses:
                    print(f"\nCourses available in the {major} major:\n")
                    for course in courses:
                        print(course)
                    course_id = input("\nEnter the Course ID you want to view grades for:\n")
                    grade = fetch_student_grade(student_id, course_id)
                    if grade:
                        print(f"\nYour grade for Course ID {course_id}: {grade[0]}")
                    else:
                        print(f"\nNo grade found for Course ID {course_id}.")
                else:
                    print(f"No courses found for the {major} major.")

            elif sub_choice == '2':
                major = input("\nYou can update grades for courses from the following majors: 'CS', 'Math', 'Biology'.\nPlease enter the major you want to update grades for:\n")
                courses = fetch_all_courses_of_major(major)
                if courses:
                    print(f"\nCourses available in the {major} major:\n")
                    for course in courses:
                        print(course)
                    course_id = input("\nEnter the Course ID you want to update grade for:\n")
                    new_grade = input("\nEnter the new grade:\n")
                    update_student_grade(student_id, course_id, new_grade)
                else:
                    print(f"No courses found for the {major} major.")

        elif choice == '6':
            print("\nYou have been successfully logged out. Have a great day!\n")
            break

        else:
            print("\nInvalid choice, please try again.\n")

if __name__ == "__main__":
    try:
        connection = sqlite3.connect('student_info_system.db')
        cursor = connection.cursor()
        main()
    finally:
        connection.close()


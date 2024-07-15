import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

connection = sqlite3.connect('student_info_system.db')
cursor = connection.cursor()

def add_student():
    id = entry_student_id.get()
    name = entry_name.get()
    enrol_year = entry_enrollment_year.get()
    major = entry_major.get()
    gender = entry_gender.get()
    cursor.execute('''
        INSERT INTO Students (StudentID, Name, EnrollmentYear, Major, Gender) 
        VALUES (?, ?, ?, ?, ?)
        ''', (id, name, enrol_year, major, gender))
    connection.commit()
    messagebox.showinfo("Success", f"Student with ID: {id} added!")

def delete_student():
    id = entry_student_id.get()
    cursor.execute('''
        DELETE FROM Students WHERE StudentID = ?
        ''', (id,))
    connection.commit()
    messagebox.showinfo("Success", f"Student with ID: {id} deleted!")

def update_student():
    id = entry_student_id.get()
    name = entry_name.get()
    enrol_year = entry_enrollment_year.get()
    major = entry_major.get()
    gender = entry_gender.get()
    cursor.execute('''
        UPDATE Students
        SET Name = ?, EnrollmentYear = ?, Major = ?, Gender = ?
        WHERE StudentID = ?
        ''', (name, enrol_year, major, gender, id))
    connection.commit()
    messagebox.showinfo("Success", f"Student with ID: {id} updated!")

def view_student_details():
    id = entry_view_student_id.get()
    cursor.execute('''
        SELECT * FROM Students WHERE StudentID = ?
        ''', (id,))
    student = cursor.fetchone()
    if student:
        details = f"ID: {student[0]}\nName: {student[1]}\nEnrollment Year: {student[2]}\nMajor: {student[3]}\nGender: {student[4]}"
        messagebox.showinfo("Student Details", details)
    else:
        messagebox.showinfo("Error", f"No student found with ID: {id}")

def add_course():
    id = entry_course_id.get()
    name = entry_course_name.get()
    major = entry_course_major.get()
    teacher_id = entry_teacher_id.get()
    cursor.execute('''
        INSERT INTO Courses (CourseID, CourseName, Major, TeacherID)
        VALUES (?, ?, ?, ?)
        ''', (id, name, major, teacher_id))
    connection.commit()
    messagebox.showinfo("Success", f"Course with ID: {id} added!")

def delete_course():
    id = entry_course_id.get()
    cursor.execute('''
        DELETE FROM Courses WHERE CourseID = ?
        ''', (id,))
    connection.commit()
    messagebox.showinfo("Success", f"Course with ID: {id} deleted!")

def update_course():
    id = entry_course_id.get()
    name = entry_course_name.get()
    major = entry_course_major.get()
    teacher_id = entry_teacher_id.get()
    cursor.execute('''
        UPDATE Courses
        SET CourseName = ?, Major = ?, TeacherID = ?
        WHERE CourseID = ?
        ''', (name, major, teacher_id, id))
    connection.commit()
    messagebox.showinfo("Success", f"Course with ID: {id} updated!")

def add_book():
    id = entry_book_id.get()
    title = entry_book_title.get()
    price = entry_book_price.get()
    cursor.execute('''
        INSERT INTO Books (BookID, Title, Price)
        VALUES (?, ?, ?)
        ''', (id, title, price))
    connection.commit()
    messagebox.showinfo("Success", f"Book with ID: {id} added!")

def delete_book():
    id = entry_book_id.get()
    cursor.execute('''
        DELETE FROM Books WHERE BookID = ?
        ''', (id,))
    connection.commit()
    messagebox.showinfo("Success", f"Book with ID: {id} deleted!")

def update_book():
    id = entry_book_id.get()
    title = entry_book_title.get()
    price = entry_book_price.get()
    cursor.execute('''
        UPDATE Books
        SET Title = ?, Price = ?
        WHERE BookID = ?
        ''', (title, price, id))
    connection.commit()
    messagebox.showinfo("Success", f"Book with ID: {id} updated!")

def assign_grade():
    stud_id = entry_grade_student_id.get()
    course_id = entry_grade_course_id.get()
    grade = entry_grade.get()
    cursor.execute('''
        INSERT OR REPLACE INTO Grades (StudentID, CourseID, Grade)
        VALUES (?, ?, ?)
        ''', (stud_id, course_id, grade))
    connection.commit()
    messagebox.showinfo("Success", f"Grade {grade} assigned to student {stud_id} for course {course_id}!")

def enroll_student():
    stud_id = entry_enroll_student_id.get()
    course_id = entry_enroll_course_id.get()
    cursor.execute('''
        INSERT INTO StudentCourses (StudentID, CourseID)
        VALUES (?, ?)
        ''', (stud_id, course_id))
    connection.commit()
    messagebox.showinfo("Success", f"Student {stud_id} enrolled in course {course_id}!")

def assign_book_to_course():
    course_id = entry_assign_course_id.get()
    book_id = entry_assign_book_id.get()
    cursor.execute('''
        INSERT INTO CourseBooks (CourseID, BookID)
        VALUES (?, ?)
        ''', (course_id, book_id))
    connection.commit()
    messagebox.showinfo("Success", f"Book {book_id} assigned to course {course_id}!")

root = tk.Tk()
root.title("Student Information System")
root.geometry("900x700")

style = ttk.Style()
style.configure('TButton', font=('Arial', 12), padding=10)
style.configure('TLabel', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

header_frame = tk.Frame(root, bg='#005b96', height=80)
header_frame.pack(fill='x')

title_label = tk.Label(header_frame, text="Student Information System", bg='#005b96', fg='white', font=('Arial', 24, 'bold'))
title_label.pack(pady=20)

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

def show_frame(frame):
    frame.tkraise()

frame_student = tk.Frame(main_frame)
frame_course = tk.Frame(main_frame)
frame_book = tk.Frame(main_frame)
frame_grade = tk.Frame(main_frame)
frame_enroll = tk.Frame(main_frame)
frame_assign = tk.Frame(main_frame)
frame_view_student = tk.Frame(main_frame)

for frame in (frame_student, frame_course, frame_book, frame_grade, frame_enroll, frame_assign, frame_view_student):
    frame.grid(row=0, column=0, sticky='nsew')

def create_student_frame():
    ttk.Label(frame_student, text="Student ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_student_id
    entry_student_id = ttk.Entry(frame_student)
    entry_student_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_student, text="Name").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_name
    entry_name = ttk.Entry(frame_student)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_student, text="Enrollment Year").grid(row=2, column=0, sticky="W", padx=5, pady=5)
    global entry_enrollment_year
    entry_enrollment_year = ttk.Entry(frame_student)
    entry_enrollment_year.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_student, text="Major").grid(row=3, column=0, sticky="W", padx=5, pady=5)
    global entry_major
    entry_major = ttk.Entry(frame_student)
    entry_major.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_student, text="Gender").grid(row=4, column=0, sticky="W", padx=5, pady=5)
    global entry_gender
    entry_gender = ttk.Entry(frame_student)
    entry_gender.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(frame_student, text="Create Student", command=add_student).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Button(frame_student, text="Delete Student", command=delete_student).grid(row=6, column=0, columnspan=2, pady=5)
    ttk.Button(frame_student, text="Update Student", command=update_student).grid(row=7, column=0, columnspan=2, pady=5)

def create_course_frame():
    ttk.Label(frame_course, text="Course ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_course_id
    entry_course_id = ttk.Entry(frame_course)
    entry_course_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_course, text="Course Name").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_course_name
    entry_course_name = ttk.Entry(frame_course)
    entry_course_name.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_course, text="Major").grid(row=2, column=0, sticky="W", padx=5, pady=5)
    global entry_course_major
    entry_course_major = ttk.Entry(frame_course)
    entry_course_major.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_course, text="Teacher ID").grid(row=3, column=0, sticky="W", padx=5, pady=5)
    global entry_teacher_id
    entry_teacher_id = ttk.Entry(frame_course)
    entry_teacher_id.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(frame_course, text="Create Course", command=add_course).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(frame_course, text="Delete Course", command=delete_course).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Button(frame_course, text="Update Course", command=update_course).grid(row=6, column=0, columnspan=2, pady=5)

def create_book_frame():
    ttk.Label(frame_book, text="Book ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_book_id
    entry_book_id = ttk.Entry(frame_book)
    entry_book_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_book, text="Title").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_book_title
    entry_book_title = ttk.Entry(frame_book)
    entry_book_title.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_book, text="Price").grid(row=2, column=0, sticky="W", padx=5, pady=5)
    global entry_book_price
    entry_book_price = ttk.Entry(frame_book)
    entry_book_price.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(frame_book, text="Create Book", command=add_book).grid(row=3, column=0, columnspan=2, pady=5)
    ttk.Button(frame_book, text="Delete Book", command=delete_book).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(frame_book, text="Update Book", command=update_book).grid(row=5, column=0, columnspan=2, pady=5)

def create_grade_frame():
    ttk.Label(frame_grade, text="Student ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_grade_student_id
    entry_grade_student_id = ttk.Entry(frame_grade)
    entry_grade_student_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_grade, text="Course ID").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_grade_course_id
    entry_grade_course_id = ttk.Entry(frame_grade)
    entry_grade_course_id.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_grade, text="Grade").grid(row=2, column=0, sticky="W", padx=5, pady=5)
    global entry_grade
    entry_grade = ttk.Entry(frame_grade)
    entry_grade.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(frame_grade, text="Assign Grade", command=assign_grade).grid(row=3, column=0, columnspan=2, pady=5)

def create_enroll_frame():
    ttk.Label(frame_enroll, text="Student ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_enroll_student_id
    entry_enroll_student_id = ttk.Entry(frame_enroll)
    entry_enroll_student_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_enroll, text="Course ID").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_enroll_course_id
    entry_enroll_course_id = ttk.Entry(frame_enroll)
    entry_enroll_course_id.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(frame_enroll, text="Enroll Student", command=enroll_student).grid(row=2, column=0, columnspan=2, pady=5)

def create_assign_frame():
    ttk.Label(frame_assign, text="Course ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_assign_course_id
    entry_assign_course_id = ttk.Entry(frame_assign)
    entry_assign_course_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_assign, text="Book ID").grid(row=1, column=0, sticky="W", padx=5, pady=5)
    global entry_assign_book_id
    entry_assign_book_id = ttk.Entry(frame_assign)
    entry_assign_book_id.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(frame_assign, text="Assign Book", command=assign_book_to_course).grid(row=2, column=0, columnspan=2, pady=5)

def create_view_student_frame():
    ttk.Label(frame_view_student, text="Student ID").grid(row=0, column=0, sticky="W", padx=5, pady=5)
    global entry_view_student_id
    entry_view_student_id = ttk.Entry(frame_view_student)
    entry_view_student_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(frame_view_student, text="View Details", command=view_student_details).grid(row=1, column=0, columnspan=2, pady=5)

create_student_frame()
create_course_frame()
create_book_frame()
create_grade_frame()
create_enroll_frame()
create_assign_frame()
create_view_student_frame()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Manage Students", command=lambda: show_frame(frame_student)).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Manage Courses", command=lambda: show_frame(frame_course)).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Manage Books", command=lambda: show_frame(frame_book)).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Assign Grades", command=lambda: show_frame(frame_grade)).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(button_frame, text="Enroll Students", command=lambda: show_frame(frame_enroll)).grid(row=0, column=4, padx=5, pady=5)
ttk.Button(button_frame, text="Assign Books", command=lambda: show_frame(frame_assign)).grid(row=0, column=5, padx=5, pady=5)
ttk.Button(button_frame, text="View Student Details", command=lambda: show_frame(frame_view_student)).grid(row=0, column=6, padx=5, pady=5)

show_frame(frame_student)

root.mainloop()
connection.close()

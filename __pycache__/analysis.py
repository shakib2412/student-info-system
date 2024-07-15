import sqlite3
connection = sqlite3.connect('student_info_system.db')
cursor = connection.cursor()

def allStudents():
    cursor.execute('''
    SELECT COUNT(*) FROM Students
    ''')
    Students = cursor.fetchall()
    for student in Students:
        print(student)
# allStudents()


def average_grade_per_course():
    cursor.execute('''
    SELECT c.CourseID, c.CourseName, AVG(CAST(g.Grade AS FLOAT)) AS AverageGrade
    FROM Courses c
    LEFT JOIN Grades g ON c.CourseID = g.CourseID
    GROUP BY c.CourseID, c.CourseName
    ''')
    courses = cursor.fetchall()
    for course in courses:
        print(course)
# average_grade_per_course()


def studentNoBook():
    cursor.execute('''
    SELECT s.StudentID, s.Name
    FROM Students s
    LEFT JOIN StudentCredits sc ON s.StudentID = sc.StudentID
    WHERE sc.Credit IS 1000;
    ''')
    students = cursor.fetchall()
    for student in students:
        print(student)
# studentNoBook()



def total_books_per_course():
    cursor.execute('''
    SELECT c.CourseID, c.CourseName, COUNT(cb.BookID) AS TotalBooks
    FROM Courses c
    LEFT JOIN CourseBooks cb ON c.CourseID = cb.CourseID
    GROUP BY c.CourseID, c.CourseName
    ''')
    courses = cursor.fetchall()
    for course in courses:
        print(course)
# total_books_per_course()


def allStudents():
    cursor.execute('''
    SELECT Name FROM Students
    ''')
    Students = cursor.fetchall()
    for student in Students:
        print(student)
# allStudents()


def top_students_by_gpa(limit=3):
    cursor.execute('''
    SELECT s.StudentID, s.Name, AVG(CAST(g.Grade AS FLOAT)) AS GPA
    FROM Students s
    LEFT JOIN Grades g ON s.StudentID = g.StudentID
    GROUP BY s.StudentID, s.Name
    ORDER BY GPA DESC
    LIMIT ?
    ''', (limit,))
    students = cursor.fetchall()
    for student in students:
        print(student)
# top_students_by_gpa(limit=3)


def courses_with_high_average_gpa(min_gpa=3.5):
    cursor.execute('''
    SELECT c.CourseID, c.CourseName, AVG(CAST(g.Grade AS FLOAT)) AS AverageGPA
    FROM Courses c
    JOIN StudentCourses sc ON c.CourseID = sc.CourseID
    JOIN Grades g ON sc.StudentID = g.StudentID
    GROUP BY c.CourseID, c.CourseName
    HAVING AVG(CAST(g.Grade AS FLOAT)) > ?
    ''', (min_gpa,))
    courses = cursor.fetchall()
    for course in courses:
        print(course)
# courses_with_high_average_gpa(min_gpa=3.5)


def students_with_books_not_enrolled():
    cursor.execute('''
    SELECT s.StudentID, s.Name
    FROM Students s
    JOIN StudentCredits sc ON s.StudentID = sc.StudentID
    WHERE sc.Credit > 0
    AND s.StudentID NOT IN (SELECT StudentID FROM StudentCourses)
    ''')
    students = cursor.fetchall()
    for student in students:
        print(student)
# students_with_books_not_enrolled()


def total_credits_per_student():
    cursor.execute('''
    SELECT s.StudentID, s.Name, COALESCE(SUM(sc.Credit), 0) AS TotalCredits
    FROM Students s
    LEFT JOIN StudentCredits sc ON s.StudentID = sc.StudentID
    GROUP BY s.StudentID, s.Name
    ''')
    students = cursor.fetchall()
    for student in students:
        print(student)
# total_credits_per_student()


def most_expensive_book_per_course():
    cursor.execute('''
    SELECT c.CourseID, c.CourseName, MAX(b.Price) AS MaxBookPrice
    FROM Courses c
    LEFT JOIN CourseBooks cb ON c.CourseID = cb.CourseID
    LEFT JOIN Books b ON cb.BookID = b.BookID
    GROUP BY c.CourseID, c.CourseName
    ''')
    courses = cursor.fetchall()
    for course in courses:
        print(course)
# most_expensive_book_per_course()


def majorCount():
    cursor.execute('''
        SELECT Major, COUNT(Major) AS StudentsIN FROM Students GROUP BY Major;
    ''')
    Majors = cursor.fetchall()
    for _ in Majors:
        print(_)
# majorCount()


def CSGrades():
    cursor.execute('''
    SELECT S.StudentID, S.Name, G.Grade 
    FROM Students S
    INNER JOIN StudentCourses SC ON S.StudentID = SC.StudentID
    INNER JOIN Grades G ON SC.StudentID = G.StudentID AND SC.CourseID = G.CourseID
    WHERE S.Major = 'CS'
    ''')
    Grades = cursor.fetchall()
    for grade in Grades:
        print(grade)
# CSGrades()


def courseMajor():
    majors = ['CS', 'Math', 'Biology', 'Physics', 'Chemistry']
    for major in majors:
        cursor.execute('''
            SELECT Major, COUNT(CourseID) AS numOfCourses  FROM Courses
            WHERE Major = ?
        ''', (major,))
        numCourses = cursor.fetchall()
        for _ in numCourses:
            print(_)
# courseMajor()


def GenderRatio():
    cursor.execute('''
    SELECT Gender , COUNT(*) FROM Students
    GROUP BY Gender
    ''')
    genderNum = cursor.fetchall()
    for gendern in genderNum:
        print(gendern)
# GenderRatio()


def avgGradeByMajor():
    cursor.execute('''
    SELECT S.Major, AVG(CAST(SC.Grade AS INTEGER)) as AvgGrade
    FROM Students S
    INNER JOIN Grades SC ON S.StudentID = SC.StudentID
    GROUP BY S.Major;
    ''')
    avgGrades = cursor.fetchall()
    for avgGrade in avgGrades:
        print(avgGrade)
# avgGradeByMajor()


def top3CoursesByAvgGrade():
    cursor.execute('''
    SELECT C.CourseName, AVG(CAST(G.Grade AS INTEGER)) as AvgGrade
    FROM Courses C
    INNER JOIN Grades G ON C.CourseID = G.CourseID
    GROUP BY C.CourseName
    ORDER BY AvgGrade DESC
    LIMIT 3;
    ''')
    topCourses = cursor.fetchall()
    for course in topCourses:
        print(course)
# top3CoursesByAvgGrade()


def coursesByTeacher():
    cursor.execute('''
    SELECT T.TeacherID, T.FirstName, T.LastName, C.CourseName, COUNT(SC.StudentID) as NumStudents
    FROM Teachers T
    INNER JOIN Courses C ON T.TeacherID = C.TeacherID
    INNER JOIN StudentCourses SC ON C.CourseID = SC.CourseID
    GROUP BY T.TeacherID, T.FirstName, T.LastName, C.CourseName;
    ''')
    teacherCourses = cursor.fetchall()
    for course in teacherCourses:
        print(course)
# coursesByTeacher()


def avgBookPriceByMajor():
    cursor.execute('''
    SELECT C.Major, AVG(B.Price) as AvgBookPrice
    FROM Courses C
    INNER JOIN CourseBooks CB ON C.CourseID = CB.CourseID
    INNER JOIN Books B ON CB.BookID = B.BookID
    GROUP BY C.Major;
    ''')
    avgBookPrices = cursor.fetchall()
    for price in avgBookPrices:
        print(price)
# avgBookPriceByMajor()


def genderDistributionByMajor():
    cursor.execute('''
    SELECT S.Major, S.Gender, COUNT(*) as NumStudents
    FROM Students S
    GROUP BY S.Major, S.Gender
    ORDER BY S.Major, S.Gender;
    ''')
    genderDistribution = cursor.fetchall()
    for distribution in genderDistribution:
        print(distribution)
# genderDistributionByMajor()



connection.close()
import sys
from os.path import dirname, join
sys.path.append(dirname(dirname(__file__)))

from app.database import SessionLocal
from app.models import User, Student, Course, Enrollment
from app.auth import get_password_hash
db = SessionLocal()

# Create admin user
if not db.query(User).filter(User.username == "admin").first():
    db.add(User(
        username="admin",
        hashed_password=get_password_hash("admin123")
    ))

# Create sample students
students = [
    {"name": "John Doe", "email": "john@college.edu", "department": "Computer Science"},
    {"name": "Jane Smith", "email": "jane@college.edu", "department": "Mathematics"}
]

for student in students:
    if not db.query(Student).filter(Student.email == student["email"]).first():
        db.add(Student(**student))

# Create sample courses
courses = [
    {"name": "Advanced Programming", "code": "CS501", "credits": 4},
    {"name": "Database Systems", "code": "CS502", "credits": 3}
]

for course in courses:
    if not db.query(Course).filter(Course.code == course["code"]).first():
        db.add(Course(**course))

db.commit()

# Create enrollments
enrollments = [
    {"student_id": 1, "course_id": 1, "semester": "Fall 2023"},
    {"student_id": 2, "course_id": 2, "semester": "Fall 2023"}
]

for enrollment in enrollments:
    if not db.query(Enrollment).filter(
        Enrollment.student_id == enrollment["student_id"],
        Enrollment.course_id == enrollment["course_id"],
        Enrollment.semester == enrollment["semester"]
    ).first():
        db.add(Enrollment(**enrollment))

db.commit()
db.close()
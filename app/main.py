from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, create_access_token, get_password_hash, verify_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

# This line must come BEFORE route definitions
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="College Management System API",
    description="API for managing students, courses, and enrollments",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add your routes here (must be after app initialization)
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Your existing login implementation
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, create_access_token, get_password_hash, verify_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

# This line must come BEFORE route definitions
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="College Management System API",
    description="API for managing students, courses, and enrollments",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add your routes here (must be after app initialization)
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Your existing login implementation
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@app.post("/courses/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
def create_course(
    course: schemas.CourseCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

# Enrollment endpoints
@app.post("/enrollments/", response_model=schemas.Enrollment, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    enrollment: schemas.EnrollmentCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    # Check if student exists
    student = db.query(models.Student).filter(
        models.Student.id == enrollment.student_id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = db.query(models.Course).filter(
        models.Course.id == enrollment.course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if enrollment already exists
    db_enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id,
        models.Enrollment.semester == enrollment.semester
    ).first()
    if db_enrollment:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course for the semester")
    
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@app.get("/enrollments/", response_model=List[schemas.Enrollment])
def read_enrollments(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    enrollments = db.query(models.Enrollment).offset(skip).limit(limit).all()
    return enrollments

@app.get("/students/{student_id}/enrollments", response_model=List[schemas.Enrollment])
def read_student_enrollments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).all()
    return enrollments
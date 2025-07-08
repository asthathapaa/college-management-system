from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, create_access_token, get_password_hash, verify_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Database tables creation
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="College Management System API",
    description="API for managing students, courses, and enrollments",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
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

# Student endpoints
@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    # Check if email already exists
    db_student = db.query(models.Student).filter(
        models.Student.email == student.email
    ).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, 
    limit: int = 100,
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    query = db.query(models.Student)
    if department:
        query = query.filter(models.Student.department == department)
    students = query.offset(skip).limit(limit).all()
    return students

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for field, value in student.dict().items():
        setattr(db_student, field, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Course endpoints (similar CRUD operations)
# ... [include all your existing course endpoints] ...

# Enhanced Enrollment endpoints
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
    
    # Check for existing enrollment
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id,
        models.Enrollment.semester == enrollment.semester
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate enrollment")
    
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@app.get("/courses/{course_id}/students", response_model=List[schemas.Student])
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    students = db.query(models.Student).join(models.Enrollment).filter(
        models.Enrollment.course_id == course_id
    ).all()
    return students

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Search endpoint
@app.get("/search/students", response_model=List[schemas.Student])
def search_students(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    return db.query(models.Student).filter(
        models.Student.name.ilike(f"%{q}%") |
        models.Student.email.ilike(f"%{q}%") |
        models.Student.department.ilike(f"%{q}%")
    ).all()
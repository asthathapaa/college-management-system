from fastapi import FastAPI, Depends, HTTPException, status
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, create_access_token, get_password_hash, verify_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="College Management System API",
    description="API for managing students, courses, and enrollments",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not verify_password(form_data.password, user.hashed_password):
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

@app.post("/students/", 
         response_model=schemas.Student,
         status_code=status.HTTP_201_CREATED)
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


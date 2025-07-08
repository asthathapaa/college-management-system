# Title: College Management System  
---  
> **Name:** Astha Thapa  
> **Roll no:** 221707  
> **Department:** BE Software Engineering  
> **Semester:** Sixth (6th)  
> **Elective Subject:** Web Services  

## Introduction

This project is a **College Management System** backend API built with **FastAPI**. It provides RESTful endpoints to manage students, courses, and enrollments with secure JWT-based authentication. The project uses **PostgreSQL** as the database, managed with SQLAlchemy ORM. The entire backend and database are containerized with **Docker** and orchestrated using **docker-compose**.

## Objectives

- Develop a secure and scalable REST API to manage college data.  
- Implement JWT authentication with password hashing.  
- Use SQLAlchemy for ORM and PostgreSQL for persistence.  
- Containerize the backend and database for easy deployment.  
- Provide API documentation via FastAPI's built-in Swagger UI.  
- Include pgAdmin container for database inspection.
 
## How to Run the Project

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/asthathapaa/college-management-system.git
   cd college-management-system

2. Docker Deployment Instructions

## Start the Docker Containers

```bash
docker-compose up -d --build

3. Access the Services

- **API Documentation:** `http://localhost:8000/docs`  
- **pgAdmin (PostgreSQL GUI):** `http://localhost:5050`  

### Default pgAdmin Credentials
**Email:** `admin@admin.com`  
**Password:** `admin`  

### Authentication
1. **Get JWT Token** from `/token` endpoint using:
   - **Username:** `admin`
   - **Password:** `admin123`

2. **Use the token** to access protected endpoints:
   - `/students/`
   - `/courses/`
   - `/enrollment/`

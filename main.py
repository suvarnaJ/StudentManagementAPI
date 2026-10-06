from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Student Management System",
    description="CRUD APIs using FastAPI and Python data structures",
    version="1.0.0"
)


# ---------------------------------------------------------
# Pydantic model for creating/replacing a student
# ---------------------------------------------------------

class Student(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    age: int = Field(
        ...,
        ge=1,
        le=100
    )

    course: str = Field(
        ...,
        min_length=3,
        max_length=50
    )


# ---------------------------------------------------------
# Pydantic model for PATCH
# All fields are optional
# ---------------------------------------------------------

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50
    )

    age: Optional[int] = Field(
        None,
        ge=1,
        le=100
    )

    course: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50
    )


# ---------------------------------------------------------
# In-memory student data
# ---------------------------------------------------------

students = {
    1: {
        "id": 1,
        "name": "Rahul",
        "age": 21,
        "course": "Data Science"
    },

    2: {
        "id": 2,
        "name": "Priya",
        "age": 22,
        "course": "Computer Science"
    },

    3: {
        "id": 3,
        "name": "Amit",
        "age": 20,
        "course": "Backend Development"
    }
}


# ---------------------------------------------------------
# Helper function to generate next ID
# ---------------------------------------------------------

def get_next_id():
    if not students:
        return 1

    return max(students.keys()) + 1


# =========================================================
# HOME API
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Student Management System",
        "documentation": "/docs"
    }


# =========================================================
# 1. POST /students
# Create a new student
# =========================================================

@app.post(
    "/students",
    status_code=201
)
def create_student(student: Student):

    new_id = get_next_id()

    new_student = {
        "id": new_id,
        "name": student.name,
        "age": student.age,
        "course": student.course
    }

    students[new_id] = new_student

    return {
        "message": "Student created successfully",
        "student": new_student
    }


# =========================================================
# 2. GET /students
# List all students
# =========================================================

@app.get("/students")
def get_students(
    course: Optional[str] = Query(
        None,
        description="Filter students by course"
    )
):

    student_list = list(students.values())

    # Optional query parameter filtering
    if course:

        student_list = [
            student
            for student in student_list
            if student["course"].lower() == course.lower()
        ]

    return {
        "count": len(student_list),
        "students": student_list
    }


# =========================================================
# 3. GET /students/{id}
# Get one student
# =========================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    return students[student_id]


# =========================================================
# 4. PUT /students/{id}
# Replace the complete student
# =========================================================

@app.put("/students/{student_id}")
def replace_student(
    student_id: int,
    student: Student
):

    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    updated_student = {
        "id": student_id,
        "name": student.name,
        "age": student.age,
        "course": student.course
    }

    students[student_id] = updated_student

    return {
        "message": "Student replaced successfully",
        "student": updated_student
    }


# =========================================================
# 5. PATCH /students/{id}
# Partially update student
# =========================================================

@app.patch("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentUpdate
):

    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    # Convert only fields supplied by the user
    update_data = student.model_dump(
        exclude_unset=True
    )

    if not update_data:

        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    # Update only supplied fields
    students[student_id].update(update_data)

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


# =========================================================
# 6. DELETE /students/{id}
# Delete student
# =========================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "student": deleted_student
    }
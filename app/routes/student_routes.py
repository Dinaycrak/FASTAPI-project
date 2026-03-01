from fastapi import APIRouter
from typing import List
from controllers.student_controller import StudentController
from models.student_model import Student

router = APIRouter()

student_controller = StudentController()


@router.post("/students")
async def create_student(student: Student):
    return student_controller.create_student(student)


@router.get("/students/{student_id}")
async def get_student(student_id: int):
    return student_controller.get_student(student_id)


@router.get("/students")
async def get_students():
    return student_controller.get_students()


@router.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    return student_controller.update_student(student_id, student)


@router.delete("/students/{student_id}")
async def delete_student(student_id: int):
    return student_controller.delete_student(student_id)
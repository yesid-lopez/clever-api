from fastapi import APIRouter

from study_buddy.models.course import Course
from study_buddy.services import course_service

router = APIRouter()


@router.post("/course")
def save_course(course: Course):
    course_id = course_service.save(course)
    return {"course_id": course_id}


@router.get("/course/{course_id}")
def find_course(course_id: str):
    course = course_service.find_course(course_id)
    return course

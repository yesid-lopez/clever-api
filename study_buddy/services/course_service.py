from study_buddy.models.course import Course
from study_buddy.repositories import course_repository
from study_buddy.services import embeddings_service


def save(course: Course) -> str:
    embeddings_service.create_collections(course.files)
    course_id = course_repository.save(course)
    return course_id


def find_course(course_id: str) -> Course:
    created_course = course_repository.find_by_id(course_id)
    return created_course

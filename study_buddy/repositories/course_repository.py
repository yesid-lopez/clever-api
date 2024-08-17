import json

from bson import ObjectId

from study_buddy.models.course import Course
from study_buddy.utils.database import course_collection


def save(course: Course):
    new_course = course_collection.insert_one(
        json.loads(course.model_dump(exclude={"id"}))
    )
    return str(new_course.inserted_id)


def find_by_id(_id: str) -> Course:
    created_course = course_collection.find_one({"_id": ObjectId(_id)})
    return Course(**created_course)

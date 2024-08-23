from bson import ObjectId

from clever.models.question import Question
from clever.utils.database import question_collection


def save(question: Question):
    saved_question = question_collection.insert_one(
        question.model_dump(exclude={"id"})
    )
    return str(saved_question.inserted_id)


def find_by_id(_id: str) -> Question:
    created_question = question_collection.find_one({"_id": ObjectId(_id)})
    return Question(**created_question)


def find_by_course(course_id: str) -> list[Question]:
    raw_questions = question_collection.find({"course_id": course_id})
    questions = [Question(**raw_question) for raw_question in raw_questions]
    return questions

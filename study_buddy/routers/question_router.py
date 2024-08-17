import json

from fastapi import APIRouter

from study_buddy.models.ask_body import AskBody
from study_buddy.models.question import Question
from study_buddy.services import question_service, visual_qa_service

router = APIRouter()


@router.post("/question/ask", tags=["Question"])
def ask_question(ask_body: AskBody):
    answer = question_service.ask(ask_body.files, ask_body.question)
    question = Question(
        question=ask_body.question, answer=answer, course_id=ask_body.course_id
    )
    question_service.save_question(question)
    return json.loads(question.json(exclude={"course_id"}))


@router.get("/question", tags=["Question"])
def get_all_questions(course_id: str):
    questions = question_service.find_by_course(course_id)
    return questions


@router.post("/question/ask-with-image", tags=["Question"])
def ask_with_image(course_id: str, file: UploadFile = File(...)):
    text, questionary = visual_qa_service.visual_qa(course_id, file)
    return {"text": text, "questionary": questionary}

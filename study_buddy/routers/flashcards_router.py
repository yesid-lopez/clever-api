from fastapi import APIRouter, HTTPException

from study_buddy.models.generate_flashcards_body import GenerateFlashcardsBody
from study_buddy.services import flashcard_service

router = APIRouter()


@router.post("/flashcards/generate", tags=["Flashcards"])
def generate_flashcards(generate_flashcards_body: GenerateFlashcardsBody):
    flashcards = flashcard_service.generate(
        sources=generate_flashcards_body.files,
        number=generate_flashcards_body.flashcards_per_file,
    )
    if not flashcards.flash_cards:
        raise HTTPException(
            status_code=404,
            detail=f"No flashcards generated for {generate_flashcards_body.files}",
        )
    flashcard_service.save_all(flashcards, generate_flashcards_body.course_id)
    return flashcards


@router.get("/flashcards", tags=["Flashcards"])
def get_all_flashcards(course_id: str):
    questions = flashcard_service.find_by_course(course_id)
    return questions

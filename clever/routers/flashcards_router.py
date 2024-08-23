from fastapi import APIRouter, HTTPException

from clever.models.generate_flashcards_body import GenerateFlashcardsBody
from clever.services import flashcard_service

router = APIRouter()


@router.post("/flashcards/generate")
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


@router.get("/flashcards")
def get_all_flashcards(course_id: str):
    questions = flashcard_service.find_by_course(course_id)
    return questions

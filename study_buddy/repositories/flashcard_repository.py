from study_buddy.models.flashcards import Flashcard, Flashcards
from study_buddy.utils.database import flashcard_collection


def save_many(flashcards: Flashcards, course_id: str):
    saved_questions = flashcard_collection.insert_many(
        [
            Flashcard(
                back=flashcard.back,
                front=flashcard.front,
                course_id=course_id,
            ).model_dump(exclude={"id"})
            for flashcard in flashcards.flash_cards
        ]
    )
    return str(saved_questions.inserted_ids)


def find_by_course(course_id: str) -> list[Flashcard]:
    raw_flashcards = flashcard_collection.find({"course_id": course_id})
    flashcards = [
        Flashcard(**raw_flashcard) for raw_flashcard in raw_flashcards
    ]
    return flashcards

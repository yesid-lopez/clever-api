import logging

from llama_index.core import Document
from pydantic import TypeAdapter

from clever.models.flashcards import (
    Flashcards,
    RawFlashcard,
    RawFlashcards,
)
from clever.repositories import flashcard_repository
from clever.services import file_service
from clever.services.embeddings_service import get_documents
from clever.utils.llama_indices import CustomSummaryIndex

logger = logging.getLogger(__name__)


def generate(sources: list[str], number=5):
    returned_flashcards = RawFlashcards()
    for file_id in sources:
        documents = get_documents(file_service.find_file(file_id))
        flashcards = _generate(documents, number)
        if flashcards:
            returned_flashcards.flash_cards = (
                flashcards + returned_flashcards.flash_cards
            )
    return returned_flashcards


def _generate(documents: list[Document], number: int):
    query = (
        "Make a list of questions and answers that are defined in the context,"
        "with one pair on each line. "
        f"Generate at least {number} questions."
        "If a question is missing it's answer, use your best judgment. "
        "Return a list of JSON objects:\n"
        '[{"front": <question>, "back": <answer>}]'
    )

    response = None
    retries = 0
    ta = TypeAdapter(list[RawFlashcard])

    while not response and retries < 3:
        try:
            response = CustomSummaryIndex(documents).query(query)
            response = ta.validate_json(response.response)
        except Exception:
            logger.exception(
                f"Failed to generate flashcards,retrying again. Retry number {retries}"
            )
            retries += 1
    return response


def save_all(flashcards: Flashcards, course_id):
    return flashcard_repository.save_many(flashcards, course_id)


def find_by_course(course_id: str):
    return flashcard_repository.find_by_course(course_id)

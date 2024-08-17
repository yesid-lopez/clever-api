from llama_index import Document

from study_buddy.models.flashcards import Flashcards, RawFlashcards
from study_buddy.repositories import flashcard_repository
from study_buddy.services import file_service
from study_buddy.services.embeddings_service import get_documents
from study_buddy.utils.llama_indices import CustomSummaryIndex


def generate(sources: list[str], number=5):
    returned_flashcards = RawFlashcards()
    for file_id in sources:
        documents = get_documents(file_service.find_file(file_id))
        flashcards = _generate(documents, number)
        if flashcards:
            returned_flashcards.flash_cards = (
                flashcards.flash_cards + returned_flashcards.flash_cards
            )
    return returned_flashcards


def _generate(documents: list[Document], number: int):
    query = (
        "Make a list of questions and answers that are defined in the context,"
        "with one pair on each line. "
        f"Generate at least {number} questions."
        "If a question is missing it's answer, use your best judgment. "
        "Write each line as as follows:\nfront: <question> back: <answer>"
    )

    response = None
    retries = 0
    while not response and retries < 3:
        try:
            response = CustomSummaryIndex(documents).query(
                query, output_class=RawFlashcards
            )
            response = response.response
        except Exception:
            retries += 1
    return response


def save_all(flashcards: Flashcards, course_id):
    return flashcard_repository.save_many(flashcards, course_id)


def find_by_course(course_id: str):
    return flashcard_repository.find_by_course(course_id)

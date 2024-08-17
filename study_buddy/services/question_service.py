from study_buddy.models.question import Question
from study_buddy.repositories import question_repository
from study_buddy.services.file_service import find_file
from study_buddy.utils.query_engine import get_query_engine

# from study_buddy.utils.trulens import TrulensClient
from study_buddy.utils.vector_store import VectorStore


def ask(files: list[str], question: str):
    collections = [
        find_file(file_id).embeddings_collection for file_id in files
    ]
    vector_store = VectorStore()
    vector_stores = [
        vector_store.load_vector_store(collection) for collection in collections
    ]

    query_engine = get_query_engine(vector_stores)

    # tru_query_engine_recorder = TrulensClient().create_recorder(
    #     query_engine, "Questions"
    # )

    # with tru_query_engine_recorder:
    #     response = query_engine.query(question)
    response = query_engine.query(question)

    return str(response)


def save_question(question: Question):
    question_repository.save(question)


def find_by_course(course_id: str):
    return question_repository.find_by_course(course_id)

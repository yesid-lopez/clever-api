import json

from fastapi import UploadFile
from pydantic import BaseModel, Field

from study_buddy.services import course_service
from study_buddy.services.file_service import find_file
from study_buddy.utils.cloud_vision import (convert_to_readable_text,
                                            extract_text_from_file)
from study_buddy.utils.models import get_llm
from study_buddy.utils.query_engine import get_query_engine
from study_buddy.utils.trulens import TrulensClient
from study_buddy.utils.vector_store import VectorStore


class QuestionOptions(BaseModel):
    question: str
    options: list[str]
    answer: str = Field(default=None)


def format_questionary(extracted_text: str):
    query = (
        "Consider the following text that has been extracted from an image:"
        f"{extracted_text}"
        "Make a list of questions and it's options that are in the context, with one pair on each line. "
        "If there are no options do not include the question either."
        "Write the output as a JSON object the following is an example:"
        '[{"question": <question>, "options": [<option_1>, <option_2>, ...] }, ...]'
    )
    questionary = []
    retries = 0
    response = None
    modified_response = ""
    while not questionary and retries < 4:
        try:
            llm = get_llm()
            response = llm.complete(query)
            modified_response = _remove_quotes(response.text)
            raw_list_question_options = json.loads(modified_response)
            print(f"json loaded successfully: {raw_list_question_options}")
            questionary = [
                QuestionOptions(**raw_question_options)
                for raw_question_options in raw_list_question_options
            ]

        except Exception as e:
            print(e)
            if response:
                print(f"error {response.text}")
                print(f"modified_response {modified_response}")
            print(
                f"Questionary generation failed, retrying one more time... Total retries {retries}"
            )
            retries += 1
    return questionary


def _remove_quotes(output: str):
    if "```json" in output:
        output = output.replace("```json", "")
    if "```" in output:
        output = output.replace("```", "")
    output = output.replace("\n", "")
    return output


def ask_question(files: list[str], question_options: QuestionOptions):
    query = (
        f"Based on the following question: {question_options.question}"
        f"and the following options: {question_options.options}"
        "Give me the answer with an small justification"
    )
    answer = _ask(files, query)
    return answer


def _ask(files: list[str], question: str):
    collections = [
        find_file(file_id).embeddings_collection for file_id in files]
    vector_store = VectorStore()
    vector_stores = [
        vector_store.load_vector_store(collection) for collection in collections
    ]

    query_engine = get_query_engine(vector_stores)

    tru_query_engine_recorder = TrulensClient().create_recorder(
        query_engine, "Visual Questions"
    )

    with tru_query_engine_recorder:
        response = query_engine.query(question)

    return str(response)


def visual_qa(course_id: str, file: UploadFile):
    # ocr
    extracted_text = extract_text_from_file(file)
    readable_content = convert_to_readable_text(extracted_text)
    questionary = format_questionary(readable_content)

    # get sources
    file_ids = course_service.find_course(course_id).files
    for question_options in questionary:
        question_options.answer = ask_question(file_ids, question_options)
    return extracted_text, questionary

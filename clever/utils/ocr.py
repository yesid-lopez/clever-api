import shutil
from os.path import join
from tempfile import TemporaryDirectory

from fastapi import UploadFile
from llama_index.core import SimpleDirectoryReader

from clever.utils.models import get_llm, get_llm_vision


def extract_text(file_path: str):
    image_documents = SimpleDirectoryReader(input_files=[file_path]).load_data(
        show_progress=True
    )
    response = get_llm_vision().complete(
        prompt="Describe the images as an alternative text",
        image_documents=image_documents,
    )
    return response.text


def extract_text_from_file(file: UploadFile):
    with TemporaryDirectory() as tmpdirname:
        formated_name = file.filename.replace(" ", "_")
        file_path = join(tmpdirname, formated_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        text = extract_text(file_path)
        return text


def convert_to_readable_text(content: str):
    prompt = (
        "Convert the following text extracted by an OCR machine learning model"
        "into a readable text: \n"
        f"{content}"
    )

    llm = get_llm()
    return llm.complete(prompt)

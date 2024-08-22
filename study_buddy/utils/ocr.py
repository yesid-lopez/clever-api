from fastapi import UploadFile
from llama_index.core import SimpleDirectoryReader

from study_buddy.utils.models import get_llm, get_llm_vision


def extract_text(file_path: str):
    """Detects text in the file located in Google Cloud Storage or on the Web."""
    image_documents = SimpleDirectoryReader(input_files=[file_path]).load_data(
        show_progress=True
    )
    response = get_llm_vision().complete(
        prompt="Describe the images as an alternative text",
        image_documents=image_documents,
    )
    return response.text


def extract_text_from_file(file: UploadFile):
    """Detects text in the file located in Google Cloud Storage or on the Web."""

    # client = vision.ImageAnnotatorClient()
    # image = vision.Image(content=file.file.read())

    # response = client.text_detection(image=image)
    # full_text = response.full_text_annotation.text
    # return full_text
    pass


def convert_to_readable_text(content: str):
    prompt = (
        "Convert the following text extracted by an OCR machine learning model"
        "into a readable text: \n"
        f"{content}"
    )

    llm = get_llm()
    return llm.complete(prompt)

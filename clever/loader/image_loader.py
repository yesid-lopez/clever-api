from llama_index.core import Document

from clever.utils.ocr import extract_text


def get_documents(file_path):
    file_name = file_path.split("/")[-1]
    extracted_text = extract_text(file_path)
    documents = [
        Document(
            text=extracted_text,
            metadata={"page_label": "1", "file_name": file_name},
        )
    ]
    return documents

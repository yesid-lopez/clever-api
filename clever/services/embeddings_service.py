import tempfile
from os import path

from clever.clients.minio_client import MinioClient
from clever.loader import image_loader, pdf_loader
from clever.models.file import File
from clever.services import file_service
from clever.utils.vector_store import VectorStore, format_collection_name


def create_collection(file: File):
    print("starting indexing....")
    collection_name = format_collection_name(file.path)
    vector_store = VectorStore()
    vector_store.load_vector_store(collection_name)

    documents = get_documents(file)
    index = vector_store.upload_documents(documents)
    print(f"Index saved {index}")
    return collection_name


def get_documents(file):
    file_extension = file.path.split(".")[-1].lower()
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = path.join(tmpdirname, file.path)
        MinioClient().fget_file(file.path, file_path)
        # If it is an image, extract text from it
        if file_extension in ["jpg", "jpeg", "png"]:
            documents = image_loader.get_documents(file_path)
        elif file_extension in ["pdf"]:
            documents = pdf_loader.get_documents(file_path)
    return documents


def create_collections(file_ids: list[str]):
    for file_id in file_ids:
        file = file_service.find_file(file_id)
        file.embeddings_collection = create_collection(file)
        file_service.update_file(file)

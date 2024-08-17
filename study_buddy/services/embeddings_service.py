from study_buddy.loader import gcs_loader, image_loader
from study_buddy.models.file import File
from study_buddy.services import file_service
from study_buddy.utils.vector_store import VectorStore, format_collection_name


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
    if file_extension in ["jpg", "jpeg", "png"]:
        documents = image_loader.get_documents(file)
    else:
        documents = gcs_loader.get_documents(file)
    return documents


def create_collections(file_ids: list[str]):
    for file_id in file_ids:
        file = file_service.find_file(file_id)
        file.embeddings_collection = create_collection(file)
        file_service.update_file(file)

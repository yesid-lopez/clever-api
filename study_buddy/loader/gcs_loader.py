# from llama_index.core import download_loader

from study_buddy.models.file import File

# OpendalGcsReader = download_loader("OpendalGcsReader")


def get_documents(file: File):
    # loader = OpendalGcsReader(
    #     bucket="study-buddy-files",
    #     path=file.path,
    # )
    # documents = loader.load_data()
    # for doc in documents:
    #     doc.metadata["file_name"] = file.name
    # return documents
    pass

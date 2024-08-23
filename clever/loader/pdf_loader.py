from llama_index.core import SimpleDirectoryReader


def get_documents(file_path: str):
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data(
        show_progress=True
    )
    return documents

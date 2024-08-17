import os
from typing import Optional

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore

from study_buddy.utils.service_context import get_service_context


class VectorStore:

    def __init__(self):
        self.vector_store = None
        self.index_from_docs: Optional[VectorStoreIndex] = None
        self.uri = os.getenv("VECTOR_DB_URI")
        self.token = os.getenv("VECTOR_DB_TOKEN")

    def load_vector_store(self, collection_name):
        self.vector_store = TiDBVectorStore(
            collection_name=collection_name,
            uri=self.uri,
            token=self.token,
            dim=768,
        )
        return self.vector_store

    def get_storage_context(self):
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store,
        )
        return storage_context

    def _get_index_from_documents(self, documents):
        self.index_from_docs = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.get_storage_context(),
            service_context=get_service_context(),
            show_progress=True,
        )

    def upload_documents(self, documents):
        self._get_index_from_documents(documents=documents)
        return self.index_from_docs.index_id


def format_collection_name(name: str):
    return name.split("/")[-1].split(".")[0].replace("-", "_")
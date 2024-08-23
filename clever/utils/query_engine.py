from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine.retriever_query_engine import (
    RetrieverQueryEngine,
)
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.vector_stores.types import VectorStore

from clever.utils.models import get_llm
from clever.utils.service_context import get_service_context


def get_query_engine(vector_stores: list[VectorStore]):
    service_context = get_service_context()
    vector_stores_indices = [
        VectorStoreIndex.from_vector_store(
            vector_store, service_context=service_context
        )
        for vector_store in vector_stores
    ]
    retrievers = [
        vs_index.as_retriever() for vs_index in vector_stores_indices
    ]
    query_fusion_retriever = QueryFusionRetriever(
        retrievers, llm=get_llm(), use_async=False
    )

    retriever_query_engine = RetrieverQueryEngine.from_args(
        query_fusion_retriever, service_context=service_context
    )
    return retriever_query_engine

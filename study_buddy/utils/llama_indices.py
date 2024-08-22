from typing import Sequence

from llama_index.core import (
    Document,
    DocumentSummaryIndex,
    get_response_synthesizer,
)
from llama_index.core.node_parser import SentenceSplitter

from study_buddy.utils.models import get_llm


class CustomSummaryIndex:
    def __init__(self, documents=Sequence[Document]):
        response_synthesizer = get_response_synthesizer(
            response_mode="tree_summarize"
        )
        self.index_summary = DocumentSummaryIndex.from_documents(
            documents,
            llm=get_llm(),
            transformations=[
                SentenceSplitter(chunk_size=612, chunk_overlap=20)
            ],
            response_synthesizer=response_synthesizer,
            show_progress=True,
        )

    def query(self, prompt: str):
        query_engine = self.index_summary.as_query_engine(
            response_mode="tree_summarize",
        )
        return query_engine.query(prompt)

from typing import Sequence

from llama_index.core import Document, SummaryIndex

from study_buddy.utils.service_context import get_service_context


class CustomSummaryIndex:
    def __init__(self, documents=Sequence[Document]):
        self.index_summary = SummaryIndex.from_documents(
            documents, service_context=get_service_context()
        )

    def query(self, prompt: str, output_class=None):
        query_engine = self.index_summary.as_query_engine(
            response_mode="tree_summarize", output_cls=output_class
        )
        return query_engine.query(prompt)

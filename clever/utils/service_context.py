from llama_index.core import ServiceContext
from llama_index.core.node_parser import SentenceSplitter

from clever.utils.models import get_embed_model, get_llm


def get_service_context():
    node_parser = SentenceSplitter(chunk_size=612, chunk_overlap=20)

    service_context = ServiceContext.from_defaults(
        llm=get_llm(), embed_model=get_embed_model(), text_splitter=node_parser
    )
    return service_context

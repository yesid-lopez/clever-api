from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.multi_modal_llms.openai import OpenAIMultiModal


def get_embed_model():
    embed_model = OpenAIEmbedding()
    return embed_model


def get_llm():
    llm = OpenAI(model="gpt-4o")
    return llm


def get_llm_vision():
    llm = OpenAIMultiModal(
        model="gpt-4o",
    )
    return llm

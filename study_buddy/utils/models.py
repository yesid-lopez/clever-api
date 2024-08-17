from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


def get_embed_model():
    embed_model = OpenAIEmbedding()
    return embed_model


def get_llm():
    llm = OpenAI()
    return llm

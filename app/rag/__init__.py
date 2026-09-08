import os
from dotenv import load_dotenv
from pathlib import Path

from llama_index.core import Settings
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from app import get_path_folder

load_dotenv()

Settings.node_parser = SentenceWindowNodeParser(
    window_size=3,
    window_metadata_key="window_metadata"
)
Settings.embed_model = OllamaEmbedding(
    model_name=os.getenv("embed_model"),
    base_url=os.getenv("base_url"),
    api_key=os.getenv("api_key"),
)
Settings.llm = Ollama(
    model=os.getenv("model"),
    base_url=os.getenv("base_url"),
    temperature=0.1,
    request_timeout=600.0
)

rerank_llm = Ollama(
    model=os.getenv("model"),
    base_url=os.getenv("base_url"),
    temperature=0.0,
    request_timeout=300.0,
)

from .generator_retriever import save_documents
from .summarize import summarize_chunks
from .window_context import create_retriever, retriever_chunks

__all__ = [
    'save_documents',
    'summarize_chunks',
    'create_retriever',
    'retriever_chunks',
]
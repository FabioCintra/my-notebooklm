import os

import chromadb
from chromadb.types import Collection
from langchain_core.retrievers import BaseRetriever
from llama_index.core import Document, SimpleDirectoryReader, VectorStoreIndex

from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from pyarrow.lib import UUID

from exceptions.exceptions import DocumentsNotFoundInFileTemp

Settings.node_parser = SentenceWindowNodeParser(
    window_size=3,
    window_metadata_key="window_metadate"
)
Settings.embed_model = OllamaEmbedding(
    model_name=os.getenv("embed_model"),
    base_url=os.getenv("base_url"),
    api_key=os.getenv("api_key"),
)

def get_vector_store(thread_id:UUID) -> ChromaVectorStore:
    path_documents_db = os.getenv("database_documents")
    os.makedirs(path_documents_db, exist_ok=True)
    chroma_client = chromadb.PersistentClient(
        path=path_documents_db
    )

    collection = chroma_client.get_or_create_collection(
        name=f"rag_{thread_id}",
    )

    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    return vector_store

def save_documents(thread_id: UUID):
    path: str = os.getenv("path_documents_name")
    list_documents: list[str] = os.listdir(path)
    if not list_documents:
        raise DocumentsNotFoundInFileTemp("None documents found in file temp")

    documents = SimpleDirectoryReader(input_files=[path]).load_data()
    merging_documents: list[Document] = Document(text="\n\n".join([doc.text for doc in documents]))

    vector_store = get_vector_store(thread_id)

    pipeline = IngestionPipeline(
        transformations=[
            Settings.node_parser,
            Settings.embed_model
        ],
        vector_store=vector_store,
    )

    pipeline.run(merging_documents)

def create_retriever(thread_id: UUID) -> BaseRetriever:
    vector_store = get_vector_store(thread_id)
    index = VectorStoreIndex(
        vector_store=vector_store,
        embedding=Settings.embed_model
    )

    retriever = index.as_retriever(
        similarity_top_k=8
    )

    return retriever

def retrieve_chunks(retriever: BaseRetriever, question: str) -> list[str]:
    results = retriever.retrieve(question)

    contents: list[str] = []
    for result in results:
        contents.append(
            result.node.get_content()
        )

    return contents






import os
from dotenv import load_dotenv

import chromadb
from llama_index.core import Document, SimpleDirectoryReader

from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.chroma import ChromaVectorStore

from pyarrow.lib import UUID

from app.exceptions import NotFound
from . import path_temp, path_embeddings

load_dotenv()

def get_vector_store(thread_id:UUID) -> ChromaVectorStore:
    chroma_client = chromadb.PersistentClient(
        path=path_embeddings
    )

    collection = chroma_client.get_or_create_collection(
        name=f"rag_{thread_id}",
    )

    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    return vector_store

def save_documents(thread_id: UUID):
    path: str = path_temp

    list_documents: list[str] = os.listdir(path)
    if not list_documents:
        raise NotFound("None documents found in file temp")

    documents = SimpleDirectoryReader(input_dir=path).load_data()
    merging_documents: Document = Document(text="\n\n".join([doc.text for doc in documents]))

    print(f"merging_documents: {merging_documents.text}")

    vector_store = get_vector_store(thread_id)

    pipeline = IngestionPipeline(
        transformations=[
            Settings.node_parser,
            Settings.embed_model
        ],
        vector_store=vector_store,
    )

    pipeline.run(documents=[merging_documents])














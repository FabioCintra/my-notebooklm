import chromadb
from pathlib import Path
from backend.app import get_path_folder
from llama_index.vector_stores.chroma import ChromaVectorStore

PATH_EMBEDDINGS = get_path_folder(Path(__file__).resolve(), "app", "storage", "embeddings")

def get_vector_store(thread_id: str) -> ChromaVectorStore:

    chroma_client = chromadb.PersistentClient(
        path=PATH_EMBEDDINGS
    )

    collection = chroma_client.get_or_create_collection(
        name=f"rag_{thread_id}",
    )

    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    return vector_store

def delete_embeddings(thread_id: str):
    client = chromadb.PersistentClient(
        path=PATH_EMBEDDINGS
    )

    collection_name = f"rag_{thread_id}"

    client.delete_collection(
        name=collection_name
    )
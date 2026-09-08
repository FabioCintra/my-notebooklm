import os
from pathlib import Path

from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline

from app import get_path_folder, delete_file_temp
from app.exceptions import NotFound
from app.repository import embeddings as EmbeddingsRepository

def save_documents(thread_id: str):
    path: str = get_path_folder(Path(__file__).resolve(), "app", "temp")

    list_documents: list[str] = os.listdir(path)
    if not list_documents:
        raise NotFound("None documents found in file temp")

    documents = SimpleDirectoryReader(input_dir=path).load_data()
    merging_documents: Document = Document(text="\n\n".join([doc.text for doc in documents]))

    vector_store = EmbeddingsRepository.get_vector_store(thread_id)

    pipeline = IngestionPipeline(
        transformations=[
            Settings.node_parser,
            Settings.embed_model
        ],
        vector_store=vector_store,
    )

    pipeline.run(documents=[merging_documents])

    #deletando documento temporario usado para gerar seus embeddings
    delete_file_temp()














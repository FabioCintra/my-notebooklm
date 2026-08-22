import os
from dotenv import load_dotenv

import chromadb
from chromadb.types import Collection
from langchain_core.retrievers import BaseRetriever
from llama_index.core import Document, SimpleDirectoryReader, VectorStoreIndex, QueryBundle, SummaryIndex, Response

from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor, LLMRerank
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from pyarrow.lib import UUID

from exceptions.exceptions import NotFound

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
    if not os.path.exists(path):
        raise NotFound("Folder 'temp' not found.")

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



def create_retriever(thread_id: UUID) -> BaseRetriever:
    vector_store = get_vector_store(thread_id)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model
    )

    retriever = index.as_retriever(
        similarity_top_k=10
    )

    return retriever

def retrieve_chunks(retriever: BaseRetriever, question: str) -> list[str]:
    nodes = retriever.retrieve(question)
    query = QueryBundle(question)

    rerank = LLMRerank(
        llm=rerank_llm,
        top_n=5,
        choice_batch_size=5
    )
    nodes_reranked = rerank.postprocess_nodes(
        nodes=nodes,
        query_bundle=query
    )

    postproc = MetadataReplacementPostProcessor(target_metadata_key="window_metadata")
    nodes_reranked_with_sentence_window = postproc.postprocess_nodes(
        nodes=nodes_reranked,
        query_bundle=query
    )

    return [
        item.node.get_content().strip()
        for item in nodes_reranked_with_sentence_window
        if item.node.get_content().strip()
    ]

def summarize_chunks(thread_id: UUID, question: str) -> str:
    vector_store = get_vector_store(thread_id)
    nodes = vector_store.get_nodes(None)

    if not nodes:
        return []

    index = SummaryIndex(
        nodes=nodes,
    )
    query_engine = index.as_query_engine(
        response_mode="tree_summarize"
    )
    result: Response = query_engine.query(question)

    return result.response













from . import rerank_llm
from .generator_retriever import get_vector_store

from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, QueryBundle
from llama_index.core.postprocessor import LLMRerank, MetadataReplacementPostProcessor

from langchain_core.retrievers import BaseRetriever
from pyarrow.lib import UUID

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

def retriever_chunks(retriever: BaseRetriever, question: str) -> list[str]:
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
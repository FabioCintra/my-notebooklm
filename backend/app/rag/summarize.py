from app.repository import embeddings as EmbeddingsRepository
from llama_index.core import SummaryIndex, Response

def summarize_chunks(thread_id: str, question: str) -> str:
    vector_store = EmbeddingsRepository.get_vector_store(thread_id)
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
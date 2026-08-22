from .generator_retriever import get_vector_store
from llama_index.core import SummaryIndex, Response
from pyarrow.lib import UUID

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
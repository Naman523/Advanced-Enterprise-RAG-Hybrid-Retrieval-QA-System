from langchain.retrievers import EnsembleRetriever
from retrievers.vector import get_vector_retriever
from retrievers.bm25 import get_bm25_retriever


def get_hybrid_retriever(
    chunks,
    persist_dir: str,
    k: int = 6,
    weights=(0.4, 0.6)
):
    bm25 = get_bm25_retriever(chunks, k)
    vector = get_vector_retriever(persist_dir, k)

    return EnsembleRetriever(
        retrievers=[bm25, vector],
        weights=list(weights)
    )

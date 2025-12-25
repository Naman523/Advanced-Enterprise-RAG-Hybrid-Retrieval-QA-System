from sentence_transformers import CrossEncoder
from typing import List

_reranker = None


def get_reranker(
    model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
):
    """
    Lazy-load cross encoder to avoid reloading on every request
    """
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(model_name)
    return _reranker


def rerank(
    query: str,
    docs: List,
    top_k: int = 5,
    max_candidates: int = 10
):
    """
    Rerank retrieved documents using cross-encoder.

    Args:
        query: user query
        docs: retrieved documents
        top_k: final docs to return
        max_candidates: number of docs to rerank

    Returns:
        List of top_k reranked documents
    """

    if not docs:
        return []

    # Limit reranking window
    docs = docs[:max_candidates]

    if len(docs) <= top_k:
        return docs

    reranker = get_reranker()

    pairs = [(query, d.page_content) for d in docs]
    scores = reranker.predict(pairs)

    ranked_docs = sorted(
        zip(scores, docs),
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for _, doc in ranked_docs[:top_k]]

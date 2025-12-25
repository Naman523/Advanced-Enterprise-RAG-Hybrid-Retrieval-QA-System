import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from typing import Dict, List

from retrievers.hybrid import get_hybrid_retriever
from retrievers.reranker import rerank
from pipelines.query_expansion import expand_query
from llm.local_llm import get_llm

from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


# ==================== PATH ====================
CHROMA_PATH = "embeddings/chroma"


# ==================== EMBEDDINGS ====================
class MPNetEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def embed_documents(self, texts: List[str]):
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str):
        return self.model.encode(text).tolist()


# ==================== GLOBAL OBJECTS ====================
_llm = None
_vectorstore = None
_retriever = None


# ==================== INITIALIZATION ====================
def initialize():
    global _llm, _vectorstore, _retriever

    if _llm is None:
        _llm = get_llm()

    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=MPNetEmbeddings()
        )

    if _retriever is None:
        data = _vectorstore.get(include=["documents", "metadatas"])
        docs = [
            type("Doc", (), {
                "page_content": d,
                "metadata": m
            })()
            for d, m in zip(data["documents"], data["metadatas"])
        ]

        _retriever = get_hybrid_retriever(
            chunks=docs,
            persist_dir=CHROMA_PATH,
            k=6
        )


# ==================== ASK FUNCTION ====================
def ask(query: str) -> Dict:
    """
    Simple, stable document-grounded RAG:
    - No modes
    - No auto-detection
    - No over-constraint
    """

    initialize()

    # -------- Query Expansion --------
    queries = expand_query(query)

    # -------- Retrieval --------
    retrieved_docs = []
    for q in queries:
        retrieved_docs.extend(
            _retriever.get_relevant_documents(q)
        )

    # -------- Deduplication --------
    unique_docs = list(
        {d.page_content: d for d in retrieved_docs}.values()
    )

    # -------- Reranking (safe fallback) --------
    try:
        top_docs = rerank(
            query=query,
            docs=unique_docs,
            top_k=5,
            max_candidates=10
        )
    except Exception:
        top_docs = unique_docs[:5]

    # -------- Context --------
    context = "\n\n".join(doc.page_content for doc in top_docs)

    # -------- SIMPLE & STABLE PROMPT --------
    prompt = f"""
You are a document-based assistant.

Instructions:
- Answer using ONLY the information present in the context.
- If the question asks for a list, list only the relevant items found.
- Do NOT include unrelated information.
- If the answer is not found at all, say: "Not found in documents."

Context:
{context}

Question:
{query}
"""

    # -------- LLM Call --------
    answer = _llm.invoke(prompt)

    # -------- Sources --------
    sources = [
        {
            "source": d.metadata.get("source", "unknown"),
            "page": d.metadata.get("page", "N/A")
        }
        for d in top_docs
    ]

    return {
        "answer": answer,
        "sources": sources
    }

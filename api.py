from fastapi import FastAPI, Query
from rag_chain import ask

app = FastAPI(
    title="AstraRAG API",
    description="Enterprise-grade RAG backend with hybrid retrieval and reranking",
    version="1.0.0"
)

@app.get("/ask")
def query(
    q: str = Query(..., description="User question")
):
    """
    Query the RAG system
    """
    return ask(q)

from langchain.retrievers import BM25Retriever

def get_bm25_retriever(chunks, k: int = 6):
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = k
    return bm25

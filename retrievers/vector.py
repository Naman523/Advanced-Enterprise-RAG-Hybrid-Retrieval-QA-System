from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from typing import List


# ---- Embedding wrapper (MUST match ingest.py) ----
class MPNetEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def embed_documents(self, texts: List[str]):
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str):
        return self.model.encode(text).tolist()


def get_vector_retriever(persist_dir: str, k: int = 6):
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=MPNetEmbeddings()  # 🔥 FIX
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})

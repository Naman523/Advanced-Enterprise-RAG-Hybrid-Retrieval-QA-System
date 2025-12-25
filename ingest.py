import os
 os.environ["ANONYMIZED_TELEMETRY"] = "False"
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
)
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


# -------------------- PATHS --------------------
DATA_PATH = "data/docs"
CHROMA_PATH = "embeddings/chroma"


# -------------------- CUSTOM EMBEDDING WRAPPER --------------------
class MPNetEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()


# -------------------- DOCUMENT LOADER --------------------
def load_documents():
    documents = []

    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            ext = file.lower().split(".")[-1]

            try:
                if ext == "pdf":
                    loader = PyPDFLoader(file_path)
                elif ext == "txt":
                    loader = TextLoader(file_path, encoding="utf-8")
                elif ext == "csv":
                    loader = CSVLoader(file_path)
                elif ext in ["doc", "docx"]:
                    loader = UnstructuredWordDocumentLoader(file_path)
                elif ext == "md":
                    loader = UnstructuredMarkdownLoader(file_path)
                elif ext in ["html", "htm"]:
                    loader = UnstructuredHTMLLoader(file_path)
                else:
                    continue

                docs = loader.load()

                for d in docs:
                    d.metadata.update({
                        "source": file,
                        "path": file_path,
                        "file_type": ext,
                        "page": d.metadata.get("page", 0),
                    })

                documents.extend(docs)

            except Exception as e:
                print(f"⚠️ Failed loading {file_path}: {e}")

    return documents


# -------------------- INGEST PIPELINE --------------------
def ingest():
    print("📄 Loading documents...")
    docs = load_documents()

    if not docs:
        print("⚠️ No documents found.")
        return

    print(f"📚 Loaded {len(docs)} documents")

    # ---------- SMART CHUNKING ----------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)
    print(f"✂️ Created {len(chunks)} chunks")

    # ---------- EMBEDDINGS ----------
    embeddings = MPNetEmbeddings()

    # ---------- PERSISTENT VECTOR DB ----------
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    # ---------- IDEMPOTENT ADD ----------
    existing_ids = set(vectorstore.get()["ids"])
    new_chunks = []

    for i, chunk in enumerate(chunks):
        chunk_id = f"{chunk.metadata['source']}_{chunk.metadata.get('page', 0)}_{i}"
        if chunk_id not in existing_ids:
            chunk.metadata["chunk_id"] = chunk_id
            new_chunks.append(chunk)

    if not new_chunks:
        print("✅ No new documents to ingest.")
        return

    vectorstore.add_documents(new_chunks)
    vectorstore.persist()

    print(f"✅ Ingested {len(new_chunks)} new chunks successfully")


# -------------------- ENTRY --------------------
if __name__ == "__main__":
    ingest()

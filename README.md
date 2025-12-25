📄 RAG Chatbot (Advanced & Free)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from your documents using hybrid retrieval, reranking, and a local LLM — completely free, offline, and no API keys required.



🚀 Features

📂 PDF document ingestion

🧠 Semantic search using embeddings

🔎 Hybrid retrieval (FAISS + BM25)

🎯 Reranking using cross-encoder models

🤖 Local LLM inference using Ollama

⚡ Optimized for speed with caching & conditional execution

🌐 FastAPI backend

🎨 Streamlit frontend UI

🔐 No paid APIs, runs fully locally







🏗️ Project Architecture

User
 ↓
Streamlit UI
 ↓
FastAPI Backend (/ask)
 ↓
Query Expansion (optional)
 ↓
Hybrid Retrieval (BM25 + FAISS)
 ↓
Reranking (Cross-Encoder)
 ↓
Local LLM (Ollama - llama3)
 ↓
Final Answer




📁 Folder Structure
RAG_CHATBOT/
├── api.py                  # FastAPI backend
├── ui.py                   # Streamlit frontend
├── ingest.py               # PDF ingestion & embedding creation
├── rag_chain.py            # Core RAG pipeline (optimized)
│
├── llm/
│   ├── __init__.py
│   └── local_llm.py        # Ollama LLM loader (cached)
│
├── pipelines/
│   ├── __init__.py
│   └── query_expansion.py  # Smart query expansion
│
├── retrievers/
│   ├── hybrid.py           # BM25 + FAISS retrieval
│   └── reranker.py         # Cross-encoder reranking
│
├── data/                   # Input PDFs
├── embeddings/             # FAISS vector store
├── requirements.txt
└── README.md






RAG_CHATBOT/
├── api.py                  # FastAPI backend
├── ui.py                   # Streamlit frontend
├── ingest.py               # PDF ingestion & embedding creation
├── rag_chain.py            # Core RAG pipeline (optimized)
│
├── llm/
│   ├── __init__.py
│   └── local_llm.py        # Ollama LLM loader (cached)
│
├── pipelines/
│   ├── __init__.py
│   └── query_expansion.py  # Smart query expansion
│
├── retrievers/
│   ├── hybrid.py           # BM25 + FAISS retrieval
│   └── reranker.py         # Cross-encoder reranking
│
├── data/                   # Input PDFs
├── embeddings/             # FAISS vector store
├── requirements.txt
└── README.md






🧠 How It Works (Simple Explanation)

Documents are ingested

PDFs are split into chunks

Chunks are converted into embeddings

Stored in FAISS vector database

User asks a question

Short queries may be expanded

Hybrid retrieval fetches relevant chunks

Reranker selects best chunks

LLM generates final answer using retrieved context

Optimizations

Models are loaded once

Reranking & expansion are used conditionally

Context size is limited for faster inference





🛠️ Installation & Setup


1️⃣ Clone the repository
git clone https://github.com/your-username/RAG_CHATBOT.git
cd RAG_CHATBOT



2️⃣ Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows


3️⃣ Install dependencies
pip install -r requirements.txt



4️⃣ Install & run Ollama
ollama pull llama3
ollama run llama3


📥 Ingest Documents

Place your PDFs inside the data/ folder, then run:
python ingest.py



▶️ Run the Application
Terminal 1 — Backend
uvicorn api:app

Terminal 2 — Frontend
streamlit run ui.py

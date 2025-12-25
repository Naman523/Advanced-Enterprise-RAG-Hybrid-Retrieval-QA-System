📄 RAG Chatbot (Advanced & Free)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from your documents using hybrid retrieval, reranking, and a local LLM — completely free, offline, and no API keys required.



🚀 Features

📂 Multi-format document ingestion (PDF, TXT, CSV, DOC, MD, HTML)

📤 Drag-and-drop document upload via modern React UI

🧠 Semantic search using embeddings

🔎 Hybrid retrieval (ChromaDB + BM25)

🎯 Reranking using cross-encoder models

🤖 Local LLM inference using Ollama (phi3:mini)

⚡ Optimized for speed with caching & conditional execution

🌐 FastAPI backend with full CRUD API

🎨 Modern React frontend with Tailwind CSS

🌓 Light/Dark mode support

📱 Fully responsive design

💬 Chat-style interface with Markdown rendering

🔐 No paid APIs, runs fully locally







🏗️ Project Architecture

User (React Frontend)
 ↓
FastAPI Backend
 ├── /upload (Document Upload)
 ├── /documents (List/Delete)
 └── /ask (Query RAG System)
      ↓
Query Expansion (optional)
 ↓
Hybrid Retrieval (BM25 + ChromaDB)
 ↓
Reranking (Cross-Encoder)
 ↓
Local LLM (Ollama - phi3:mini)
 ↓
Final Answer (with Sources)




📁 Folder Structure
RAG_CHATBOT/
├── api.py                      # FastAPI backend with CRUD endpoints
├── ui.py                       # Legacy Streamlit UI (optional)
├── ingest.py                   # Document ingestion & embedding
├── rag_chain.py                # Core RAG pipeline (optimized)
│
├── app/frontend/               # Modern React Frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API integration
│   │   ├── utils/              # Helper functions
│   │   └── App.jsx             # Main app
│   ├── package.json
│   └── README.md
│
├── llm/
│   ├── __init__.py
│   └── local_llm.py            # Ollama LLM loader (cached)
│
├── pipelines/
│   ├── __init__.py
│   └── query_expansion.py      # Smart query expansion
│
├── retrievers/
│   ├── hybrid.py               # BM25 + ChromaDB retrieval
│   ├── reranker.py             # Cross-encoder reranking
│   ├── vector.py               # Vector store retriever
│   └── bm25.py                 # BM25 retriever
│
├── data/docs/                  # Uploaded documents
├── embeddings/chroma/          # ChromaDB vector store
├── evaluation/                 # RAG evaluation metrics
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

Option 1: Modern React Frontend (Recommended)

Terminal 1 — Backend
uvicorn api:app --reload

Terminal 2 — Frontend
cd app/frontend
npm install  # First time only
npm run dev

Open http://localhost:3000 in your browser

Option 2: Legacy Streamlit UI

Terminal 1 — Backend
uvicorn api:app --reload

Terminal 2 — Frontend
streamlit run ui.py


🎨 Frontend Features

Modern React UI with:
- Drag-and-drop document upload
- Real-time document management
- Chat-style interface
- Markdown rendering for AI responses
- Collapsible source context
- Light/Dark mode toggle
- Fully responsive design
- Smooth animations

Backend API Endpoints:
- GET /ask?q=<query> - Ask questions
- POST /upload - Upload documents
- GET /documents - List all documents
- DELETE /documents/<filename> - Delete document


📖 Detailed Documentation

Frontend Guide: See app/frontend/README.md for detailed frontend documentation
Backend API: Visit http://localhost:8000/docs for interactive API documentation

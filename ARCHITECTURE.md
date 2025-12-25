# System Architecture

## Overview

This document provides a comprehensive overview of the RAG Document Chat application architecture.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐    │
│  │  Sidebar   │  │  Chat Area   │  │   Theme Toggle      │    │
│  │            │  │              │  │                     │    │
│  │ - Upload   │  │ - Messages   │  │ - Light/Dark        │    │
│  │ - Doc List │  │ - Input      │  │                     │    │
│  └────────────┘  └──────────────┘  └─────────────────────┘    │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              API Service Layer (Axios)                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                    http://localhost:8000                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                          │  │
│  │  • POST /upload         - Upload documents               │  │
│  │  • GET /documents       - List documents                 │  │
│  │  • DELETE /documents/   - Delete document                │  │
│  │  • GET /ask            - Query RAG system                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │              Document Management                          │  │
│  │  • File validation                                        │  │
│  │  • Storage in data/docs/                                 │  │
│  │  • Automatic ingestion                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        RAG PIPELINE                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Query Expansion (Optional)                           │  │
│  │     • Expand short queries                               │  │
│  │     • Generate alternative phrasings                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  2. Hybrid Retrieval                                     │  │
│  │     ┌─────────────────┐    ┌──────────────────┐        │  │
│  │     │  BM25 Retrieval │    │ Vector Retrieval │        │  │
│  │     │  (Keyword)      │    │  (ChromaDB)      │        │  │
│  │     └────────┬────────┘    └─────────┬────────┘        │  │
│  │              └────────┬───────────────┘                 │  │
│  │                       │ Merge Results                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  3. Reranking                                            │  │
│  │     • Cross-Encoder Model                                │  │
│  │     • Score relevance                                    │  │
│  │     • Select top-k chunks                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  4. Context Building                                     │  │
│  │     • Combine top chunks                                 │  │
│  │     • Track sources                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  5. LLM Generation                                       │  │
│  │     • Ollama (phi3:mini)                                 │  │
│  │     • Generate answer                                    │  │
│  │     • Include sources                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        DATA STORAGE                              │
│                                                                   │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │  data/docs/    │  │ embeddings/     │  │ Browser        │  │
│  │                │  │ chroma/         │  │ LocalStorage   │  │
│  │ • Uploaded     │  │                 │  │                │  │
│  │   documents    │  │ • Vector store  │  │ • Theme pref   │  │
│  │ • PDF, TXT,    │  │ • Embeddings    │  │                │  │
│  │   DOC, etc.    │  │ • Metadata      │  │                │  │
│  └────────────────┘  └─────────────────┘  └────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Component Hierarchy

```
App
├── Sidebar
│   ├── FileUpload
│   └── DocumentList
├── Header
│   └── ThemeToggle
└── ChatArea
    └── Message (multiple)
```

### Data Flow

```
User Action
    ↓
Component Handler
    ↓
API Service (services/api.js)
    ↓
Backend Endpoint
    ↓
Response
    ↓
State Update (useState)
    ↓
Re-render Components
    ↓
User Sees Result
```

## Backend Architecture

### Request Flow

```
HTTP Request
    ↓
FastAPI Router
    ↓
Endpoint Handler
    ↓
┌─────────────┬──────────────┬──────────────┐
│   Upload    │   Delete     │    Query     │
│             │              │              │
│  • Validate │  • Remove    │  • Expand    │
│  • Save     │    file      │  • Retrieve  │
│  • Ingest   │  • Reinit    │  • Rerank    │
│  • Reinit   │              │  • Generate  │
└─────────────┴──────────────┴──────────────┘
    ↓
JSON Response
```

### Document Ingestion Pipeline

```
Document File
    ↓
Document Loader (based on file type)
    ↓
Text Extraction
    ↓
Text Splitter (RecursiveCharacterTextSplitter)
    ├─ chunk_size: 500
    └─ chunk_overlap: 100
    ↓
Chunks with Metadata
    ↓
Embedding Model (all-mpnet-base-v2)
    ↓
Vector Embeddings
    ↓
ChromaDB Storage
    ↓
Indexed for Retrieval
```

### RAG Query Pipeline

```
User Query
    ↓
[Optional] Query Expansion
    ↓
Parallel Retrieval
    ├─ BM25 (keyword-based)
    └─ Vector Search (semantic)
    ↓
Merge & Deduplicate Results
    ↓
Cross-Encoder Reranking
    ↓
Top-K Selection (k=5)
    ↓
Context Assembly
    ↓
Prompt Construction
    ↓
LLM Generation (Ollama)
    ↓
Answer + Sources
```

## Technology Stack

### Frontend

```
┌────────────────────────────────────┐
│  React 18                          │
│  • Component-based UI              │
│  • Hooks for state management      │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  Vite                              │
│  • Fast dev server                 │
│  • Hot module replacement          │
│  • Optimized builds                │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  Tailwind CSS                      │
│  • Utility-first styling           │
│  • Dark mode support               │
│  • Custom theme                    │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  Axios                             │
│  • HTTP client                     │
│  • Request/response interceptors   │
│  • Upload progress tracking        │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  React Markdown                    │
│  • Markdown rendering              │
│  • Syntax highlighting             │
└────────────────────────────────────┘
```

### Backend

```
┌────────────────────────────────────┐
│  FastAPI                           │
│  • REST API framework              │
│  • Automatic API docs              │
│  • Type validation                 │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  LangChain                         │
│  • RAG orchestration               │
│  • Document loaders                │
│  • Text splitters                  │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  ChromaDB                          │
│  • Vector database                 │
│  • Embedding storage               │
│  • Similarity search               │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  Sentence Transformers             │
│  • all-mpnet-base-v2 (embeddings) │
│  • cross-encoder (reranking)       │
└────────────────────────────────────┘
         │
┌────────▼───────────────────────────┐
│  Ollama                            │
│  • phi3:mini (LLM)                 │
│  • Local inference                 │
└────────────────────────────────────┘
```

## Security Considerations

### Frontend
- Environment variables for API URL
- No sensitive data in client code
- HTTPS in production
- Input validation

### Backend
- CORS configured for frontend
- File type validation
- File size limits
- Path traversal prevention
- Error message sanitization

### Data
- Local storage only
- No external API calls (except Ollama)
- No user tracking
- No data collection

## Performance Optimizations

### Frontend
- Code splitting
- Lazy loading
- Memoization
- Optimized re-renders
- Production builds minified

### Backend
- Model caching (loaded once)
- Conditional query expansion
- Limited context size
- Efficient retrieval (k=6)
- Reranking window (top 10)

### RAG Pipeline
- Hybrid retrieval (best of both)
- Cross-encoder reranking
- Smart chunking (500 chars, 100 overlap)
- Persistent vector store
- Idempotent ingestion

## Scalability Considerations

### Current Limitations
- Single-user application
- No database (file-based)
- No authentication
- Local LLM (requires GPU/CPU)

### Scaling Options

**Horizontal:**
- Add Redis for caching
- Queue system for uploads
- CDN for frontend
- Load balancer for backend

**Vertical:**
- GPU acceleration for LLM
- Larger models
- More embeddings
- Bigger vector store

**Cloud:**
- Hosted vector DB (Pinecone, Weaviate)
- Managed LLM (OpenAI API)
- Cloud storage (S3)
- Container orchestration (Kubernetes)

## Deployment Architecture

### Development

```
localhost:3000 (Frontend)
     ↓
localhost:8000 (Backend)
     ↓
localhost:11434 (Ollama)
```

### Production

```
https://app.example.com (Frontend - CDN)
     ↓
https://api.example.com (Backend - Server)
     ↓
Internal Ollama Server (GPU)
     ↓
ChromaDB (Persistent Volume)
```

## Monitoring & Observability

### Current Status
- Console logging
- FastAPI automatic docs
- Browser DevTools
- Network tab inspection

### Production Recommendations
- Application logs (Winston, Pino)
- API monitoring (Prometheus)
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Uptime monitoring (Pingdom)

## Testing Strategy

### Frontend Testing
- Component tests (Jest, React Testing Library)
- E2E tests (Playwright, Cypress)
- Visual regression (Chromatic)

### Backend Testing
- Unit tests (pytest)
- Integration tests
- API tests (pytest + httpx)
- Load tests (Locust)

### RAG Testing
- Evaluation metrics (already implemented)
- Retrieval accuracy
- Answer quality
- Source relevance

## Maintenance & Updates

### Regular Maintenance
- Dependency updates
- Security patches
- Model updates
- Performance tuning

### Feature Additions
- See IMPLEMENTATION_SUMMARY.md for ideas
- User feedback integration
- A/B testing
- Analytics-driven improvements

## Conclusion

This architecture provides:
- Clear separation of concerns
- Scalable structure
- Modern tech stack
- Production-ready design
- Easy maintenance
- Good developer experience

All components work together to deliver a fast, reliable, and user-friendly RAG document chat experience.

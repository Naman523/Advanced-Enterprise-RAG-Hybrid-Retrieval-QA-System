# Quick Start Guide

Get your RAG Document Chat application running in 5 minutes.

## Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher
- Node.js 16 or higher
- Ollama installed ([Download here](https://ollama.ai))

## Step 1: Backend Setup

### 1.1 Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 1.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 1.3 Setup Ollama

```bash
ollama pull phi3:mini
```

### 1.4 Start Backend Server

```bash
uvicorn api:app --reload
```

Backend will run on http://localhost:8000

Verify: Open http://localhost:8000/docs to see API documentation

## Step 2: Frontend Setup

### 2.1 Install Dependencies

Open a new terminal:

```bash
cd app/frontend
npm install
```

### 2.2 Start Frontend

```bash
npm run dev
```

Frontend will run on http://localhost:3000

## Step 3: Use the Application

1. Open http://localhost:3000 in your browser
2. Upload a document (drag and drop or click to browse)
3. Wait for the upload to complete
4. Ask questions about your document
5. View AI-generated answers with source citations

## Supported File Formats

- PDF (.pdf)
- Text (.txt)
- CSV (.csv)
- Word (.doc, .docx)
- Markdown (.md)
- HTML (.html, .htm)

## Troubleshooting

### Backend Issues

**Problem:** "ModuleNotFoundError"
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

**Problem:** "Ollama not found"
**Solution:** Install and start Ollama:
```bash
ollama pull phi3:mini
ollama serve
```

**Problem:** "Port 8000 already in use"
**Solution:** Kill existing process or use different port:
```bash
uvicorn api:app --reload --port 8001
```
Then update `app/frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8001
```

### Frontend Issues

**Problem:** "npm install" fails
**Solution:** Clear npm cache:
```bash
npm cache clean --force
npm install
```

**Problem:** "CORS error"
**Solution:** Ensure backend is running with CORS enabled (already configured in api.py)

**Problem:** Upload fails
**Solution:** Check file size and format. Ensure `data/docs` directory exists.

### Common Issues

**Problem:** Questions return "Not found in documents"
**Solution:**
1. Ensure document was uploaded successfully
2. Try rephrasing your question
3. Check if the information exists in your document

**Problem:** Slow responses
**Solution:**
1. Ollama may be loading the model (first query is slower)
2. Check system resources (CPU/RAM usage)
3. Consider using a smaller model if needed

## Development Tips

### Hot Reload

Both backend and frontend support hot reload:
- Backend: Automatically reloads on file changes (--reload flag)
- Frontend: Automatically updates in browser on file changes

### View API Documentation

Visit http://localhost:8000/docs for interactive API documentation

### Test API Endpoints

Using curl:
```bash
# List documents
curl http://localhost:8000/documents

# Ask question
curl "http://localhost:8000/ask?q=What%20is%20this%20about"

# Upload document
curl -X POST -F "file=@path/to/document.pdf" http://localhost:8000/upload
```

## Production Deployment

### Backend

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
cd app/frontend

# Build production bundle
npm run build

# Serve with any static server
npx serve -s dist
```

## Next Steps

- Explore the codebase structure
- Customize the UI theme in `app/frontend/tailwind.config.js`
- Add more documents to test retrieval quality
- Check out the evaluation metrics in `evaluation/`
- Experiment with different Ollama models

## Need Help?

- Backend API docs: http://localhost:8000/docs
- Frontend README: app/frontend/README.md
- Main README: README.md

Enjoy your RAG Document Chat application!

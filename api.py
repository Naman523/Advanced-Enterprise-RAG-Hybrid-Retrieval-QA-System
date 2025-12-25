import os
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_chain import ask, reinitialize
from ingest import ingest_single_document

app = FastAPI(
    title="AstraRAG API",
    description="Enterprise-grade RAG backend with hybrid retrieval and reranking",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = "data/docs"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv", ".doc", ".docx", ".md", ".html", ".htm"}

class DocumentResponse(BaseModel):
    filename: str
    size: int
    path: str

@app.get("/ask")
def query(
    q: str = Query(..., description="User question")
):
    """
    Query the RAG system
    """
    return ask(q)

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the RAG system
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    os.makedirs(DATA_PATH, exist_ok=True)

    file_path = os.path.join(DATA_PATH, file.filename)

    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

        ingest_single_document(file_path)
        reinitialize()

        return DocumentResponse(
            filename=file.filename,
            size=file_size,
            path=file_path
        )

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/documents", response_model=List[DocumentResponse])
def list_documents():
    """
    List all uploaded documents
    """
    if not os.path.exists(DATA_PATH):
        return []

    documents = []
    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        if os.path.isfile(file_path):
            documents.append(
                DocumentResponse(
                    filename=file,
                    size=os.path.getsize(file_path),
                    path=file_path
                )
            )

    return documents

@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Delete a document from the RAG system
    """
    file_path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        os.remove(file_path)
        reinitialize()
        return {"message": f"Document {filename} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

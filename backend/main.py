from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import shutil
import tempfile

from parsers import parse_document
from chunker import chunk_text
from embedder import embed_chunks
from uploader import upload_chunks

load_dotenv()

app = FastAPI(title="ContextFlow AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ContextFlow AI backend running"}


@app.get("/health")
def health_check():
    pinecone_key = os.getenv("PINECONE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    return {
        "pinecone_key_loaded": bool(pinecone_key),
        "groq_key_loaded": bool(groq_key)
    }


# Maps uploaded file extensions to our parser's file_type labels
EXTENSION_MAP = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "txt"
}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a PDF, DOCX, or TXT file upload.
    Saves it temporarily, parses it, chunks it, embeds it,
    and stores the vectors in Pinecone.
    """
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in EXTENSION_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: pdf, docx, txt"
        )

    file_type = EXTENSION_MAP[ext]

    # Save the uploaded file to a temp location so our parsers
    # (which expect a file path) can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        text = parse_document(tmp_path, file_type)

        if not text:
            raise HTTPException(
                status_code=422,
                detail="No text could be extracted from this file."
            )

        chunks = chunk_text(text, target_size=500, overlap_sentences=1)
        embeddings = embed_chunks(chunks)
        uploaded_count = upload_chunks(
            chunks, embeddings, source=file.filename, file_type=file_type
        )

        return {
            "filename": file.filename,
            "chunks_created": len(chunks),
            "vectors_uploaded": uploaded_count
        }

    finally:
        # Clean up the temp file regardless of success/failure
        os.remove(tmp_path)


@app.post("/upload-url")
async def upload_url(url: str):
    """
    Accepts a web page URL, parses it, chunks it, embeds it,
    and stores the vectors in Pinecone.
    """
    try:
        text = parse_document(url, "url")

        if not text:
            raise HTTPException(
                status_code=422,
                detail="No text could be extracted from this URL."
            )

        chunks = chunk_text(text, target_size=500, overlap_sentences=1)
        embeddings = embed_chunks(chunks)
        uploaded_count = upload_chunks(
            chunks, embeddings, source=url, file_type="url"
        )

        return {
            "url": url,
            "chunks_created": len(chunks),
            "vectors_uploaded": uploaded_count
        }

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
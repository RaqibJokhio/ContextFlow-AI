from pinecone import Pinecone
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)
index = pc.Index("contextflow-ai")


def upload_chunks(chunks: list[str], embeddings: list[list[float]], source: str, file_type: str):
    """
    Uploads chunks + their embeddings to Pinecone.
    Each vector gets a unique ID and metadata so we can trace
    which document/source it came from, and show the original
    text back to the user at query time.

    source: filename or URL the chunk came from
    file_type: 'pdf', 'docx', 'txt', or 'url'
    """
    vectors = []
    for chunk, embedding in zip(chunks, embeddings):
        vector_id = str(uuid.uuid4())
        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "text": chunk,
                "source": source,
                "file_type": file_type
            }
        })

    index.upsert(vectors=vectors)
    return len(vectors)
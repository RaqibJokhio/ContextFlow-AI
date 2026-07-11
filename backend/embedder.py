from sentence_transformers import SentenceTransformer

# Loaded once when the module is imported — reused across all calls.
# Downloads the model on first run (~80MB), then caches it locally.
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Converts a list of text chunks into a list of embedding vectors.
    Each vector is 384 dimensions, matching the Pinecone index.
    """
    embeddings = model.encode(chunks, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str) -> list[float]:
    """
    Converts a single query string into an embedding vector,
    for use at search/retrieval time.
    """
    embedding = model.encode(query, show_progress_bar=False)
    return embedding.tolist()
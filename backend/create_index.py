from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

INDEX_NAME = "contextflow-ai"
DIMENSION = 384  # matches all-MiniLM-L6-v2 output size

existing_indexes = pc.list_indexes().names()

if INDEX_NAME in existing_indexes:
    print(f"Index '{INDEX_NAME}' already exists. Skipping creation.")
else:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Index '{INDEX_NAME}' created successfully.")
from dotenv import load_dotenv
from pinecone import Pinecone
import os

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    print("ERROR: PINECONE_API_KEY not found in .env")
    exit(1)

pc = Pinecone(api_key=api_key)

try:
    indexes = pc.list_indexes()
    print("Connection successful.")
    print("Existing indexes:", indexes.names())
except Exception as e:
    print("Connection failed:", e)
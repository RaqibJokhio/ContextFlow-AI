from parsers import parse_document
from chunker import chunk_text
from embedder import embed_chunks
from uploader import upload_chunks

# Full pipeline test: parse -> chunk -> embed -> upload
text = parse_document("test_files/sample.txt", "txt")
chunks = chunk_text(text, target_size=200, overlap_sentences=1)
embeddings = embed_chunks(chunks)

print(f"Parsed text length: {len(text)} chars")
print(f"Number of chunks: {len(chunks)}")
print(f"Embedding dimension: {len(embeddings[0])}")

uploaded_count = upload_chunks(chunks, embeddings, source="sample.txt", file_type="txt")
print(f"Uploaded {uploaded_count} vectors to Pinecone.")
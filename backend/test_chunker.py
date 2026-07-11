from parsers import parse_document
from chunker import chunk_text

text = parse_document("test_files/sample.txt", "txt")

chunks = chunk_text(text, target_size=200, overlap_sentences=1)

print(f"Total chunks: {len(chunks)}\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk)
    print()
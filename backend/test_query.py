from embedder import embed_query
from uploader import index

query = "What affects the success of machine learning projects?"
query_vector = embed_query(query)

results = index.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True
)

for match in results["matches"]:
    print(f"Score: {match['score']:.4f}")
    print(f"Text: {match['metadata']['text']}")
    print(f"Source: {match['metadata']['source']}\n")
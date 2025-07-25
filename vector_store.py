from typing import List
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME

# Initialize once
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store_chunks(chunks: List[str]):
    """Store chunks in Pinecone."""
    embeddings = model.encode(chunks)
    vectors = [
        {"id": f"chunk-{i}", "values": emb.tolist(), "metadata": {"text": chunk}}
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]
    index.upsert(vectors=vectors)


def query_top_chunks(query: str, top_k=3) -> str:
    """Query similar chunks."""
    query_vec = model.encode([query])[0].tolist()
    res = index.query(vector=query_vec, top_k=top_k, include_metadata=True)
    return "\n".join([match["metadata"]["text"] for match in res["matches"]])

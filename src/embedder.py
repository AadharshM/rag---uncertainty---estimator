from sentence_transformers import SentenceTransformer
import faiss
#FAISS -> Facebook AI Similarity Search
import numpy as np

from ingest import load_Pdf
from chunker import chunk_docs


def build_vector_store(chunks):

    model =  SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts,show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks, model

def search(querry,index,chunks,model,top_k=3):
    
    querry_embedding = model.encode([querry]).astype("float32")
    distances,indices = index.search(querry_embedding,top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results

if __name__ == "__main__":
    documents = load_Pdf()
    chunks = chunk_docs(documents)

    index, chunks, model = build_vector_store(chunks)
    print(f"\n✅ Vector store built with {index.ntotal} chunks")

    query = "What is this document about?"
    results = search(query, index, chunks, model)

    print(f"\n--- Top results for: '{query}' ---")
    for r in results:
        print(f"\nSource: {r['source']} (chunk {r['id']})")
        print(r['text'][:200])

from ingest import load_Pdf

def simple_chunk_text(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap  # move forward, leaving overlap
    
    return chunks

def chunk_docs(documents, chunk_size = 500, chunk_overlap=50):
   
    all_chunks = []

    for filename,text in documents.items():
        chunks = simple_chunk_text(text, chunk_size, chunk_overlap)
        for i,chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": filename,
                "id":i
            })
    return all_chunks

if __name__ == "__main__":
    documents = load_Pdf()
    chunks = chunk_docs(documents)
    print(f"Total chunks created are {len(chunks)}")
    print("-----sample chunk------")
    print(chunks[0])

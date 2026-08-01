from langchain_groq import ChatGroq
from dotenv import load_dotenv
from ingest import load_Pdf
from chunker import chunk_docs
from embedder import build_vector_store, search
from parsing import parse_response

load_dotenv()

def vector_building():
   
    documents = load_Pdf()
    chunks = chunk_docs(documents)
    index, chunks, model = build_vector_store(chunks)
    return index, chunks, model


def get_answer(query, index, chunks, model):
   
    results = search(query, index, chunks, model)

    context = ""
    for chunk in results:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"

    llm = ChatGroq(model="llama-3.1-8b-instant")

    response = llm.invoke(f"""
    You are an AI assistant that answers questions based on documents.
    Answer ONLY from the provided context.
    After giving your answer, you must rate your own confidence as LOW, MEDIUM, or HIGH,
    and explain why you are or aren't confident in your answer.

    Context: {context}
    Question: {query}
    """)
    answer, confidence_level, reasoning = parse_response(response.content)
    return answer, confidence_level, reasoning
    


if __name__ == "__main__":
    index, chunks, model = vector_building()
    query = input("Enter the question: ")
    answer, confidence_level, reasoning = get_answer(query, index, chunks, model)
    print(f"Answer: {answer}")
    print(f"Confidence: {confidence_level}")
    print(f"Reasoning: {reasoning}")



import streamlit as st
from ingest import load_pdfs_from_uploads
from chunker import chunk_docs
from embedder import build_vector_store, search
from llm_groq import get_answer

st.set_page_config(page_title="RAG Testing", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #4338CA;
        transform: scale(1.03);
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .answer-card {
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .badge-glow {
        animation: pulseGlow 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #FAFAFA; font-size: 3rem;">🧠 RAG Testing</h1>
    <p style="color: #A0A0A0; font-size: 1.2rem;">
        Upload documents, ask questions, get answers with real confidence scoring.
    </p>
</div>
""", unsafe_allow_html=True)


def confidence_badge(level):
    level = level.upper()
    if "HIGH" in level:
        color = "#10B981"
    elif "MEDIUM" in level:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    return f"""
    <span class="badge-glow" style="
        background-color: {color}20;
        color: {color};
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 600;
        border: 1px solid {color};
    ">
        {level}
    </span>
    """
uploaded_files = st.file_uploader("Upload your PDF documents", type="pdf", accept_multiple_files=True)


@st.cache_resource
def load_vector_store(uploaded_files):
    documents = load_pdfs_from_uploads(uploaded_files)
    chunks = chunk_docs(documents)
    index, chunks, model = build_vector_store(chunks)
    return index, chunks, model

if uploaded_files:
    with st.spinner("Processing documents..."):
        index, chunks, model = load_vector_store(uploaded_files)

    st.success(f"✅ {len(uploaded_files)} document(s) processed and ready!")

    query = st.text_input("Ask a question about your documents")
    submit = st.button("Get Answer")

    if submit and query:
        with st.spinner("Searching documents and generating answer..."):
            answer, confidence_level, reasoning = get_answer(query, index, chunks, model)

        st.markdown(f"""
        <div class="answer-card" style="
            background-color: #1E1E2E;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #2A2A3E;
            margin: 1rem 0;
        ">
            <p style="color: #FAFAFA; font-size: 1.1rem; line-height: 1.6;">{answer}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Confidence Level:**")
        st.markdown(confidence_badge(confidence_level), unsafe_allow_html=True)

        with st.expander("Why this confidence level?"):
            st.write(reasoning)
else:
    st.info("👆 Upload one or more PDF documents to get started.")



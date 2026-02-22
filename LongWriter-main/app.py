import streamlit as st
import pdfplumber
import agentwrite.write as aw 

st.set_page_config(page_title="AI Handbook Generator", layout="wide")
st.title("📖 AI Handbook Generator — Free LLM Demo")
st.write("Upload PDFs, ask questions, and generate a handbook (mock RAG + OpenRouter)")

# --- Set your OpenRouter API key here ---
OPENROUTER_API_KEY = "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"

# --- Mock RAG ---
class LightRAG:
    def __init__(self):
        self.chunks = []

    def add_texts(self, texts):
        self.chunks.extend(texts)

    def query(self, question, top_k=5):
        question_words = question.lower().split()
        matched = [c for c in self.chunks if any(w in c.lower() for w in question_words)]
        if not matched:
            matched = self.chunks
        return [{"text": c} for c in matched[:top_k]]

# --- Helpers ---
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# --- Session state ---
if "rag" not in st.session_state:
    st.session_state.rag = LightRAG()
if "all_chunks" not in st.session_state:
    st.session_state.all_chunks = []

# --- PDF upload ---
uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    all_text = ""
    for uploaded_file in uploaded_files:
        st.write(f"Processing: {uploaded_file.name}")
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

    chunks = chunk_text(all_text)
    st.session_state.rag.add_texts(chunks)
    st.session_state.all_chunks = chunks
    st.success(f"Indexed {len(chunks)} chunks into mock RAG.")

# --- Chat input ---
st.subheader("Ask a question about the PDFs")
user_question = st.text_input("Your question")

if user_question:
    results = st.session_state.rag.query(user_question, top_k=5)
    st.subheader("Retrieved context (mock RAG)")
    for i, r in enumerate(results):
        st.write(f"Result {i+1}:")
        st.write(r["text"])

# --- Handbook generation ---
st.subheader("Generate Handbook (Free LLM)")

if st.button("Generate 20,000-word handbook"):
    if not st.session_state.all_chunks:
        st.warning("Upload PDFs first!")
    else:
        st.info("Generating handbook using OpenRouter... this may take a few minutes")
        
        context_text = "\n".join(st.session_state.all_chunks)
        
        plan_text = "1. Create Table of Contents\n2. Summarize each section\n3. Include citations from text"

        prompt = f"Create a 20,000-word handbook from the following content:\n\n{context_text}\n\nPlan:\n{plan_text}"

        handbook_text = aw.get_response_openrouter(prompt, max_tokens=512, api_key=OPENROUTER_API_KEY)

        st.text_area("Handbook Output : ", handbook_text, height=600)
        st.success("Handbook generated ")
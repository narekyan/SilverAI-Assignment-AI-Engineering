📘 AI Handbook Generator (Streamlit + OpenRouter)

This project is a simple AI-powered application that allows users to:

Upload PDF documents

Ask questions about their content

Generate a long structured handbook (10k–20k+ words) from the uploaded PDFs

The app uses Streamlit for the UI and a free OpenRouter model for text generation.

📂 Project Files
app.py

Main Streamlit application:

Handles PDF upload

Extracts text from PDFs

Provides a simple chat interface

Sends prompts to the LLM

Displays the generated handbook

Allows downloading the generated handbook

agentwrite/write.py

LLM interaction logic:

Contains the function that calls the OpenRouter API

Sends prompts and receives generated text

Controls max_tokens to respect free-tier limits

Can be extended to support chunked generation

🚀 How to Run the App
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Set your OpenRouter API key (inline)

Open agentwrite/write.py and set your API key directly:

OPENROUTER_API_KEY = "your_openrouter_api_key_here"

You can get a free API key from:
https://openrouter.ai

3️⃣ Run the application
streamlit run app.py

Then open your browser at:

http://localhost:8501
🤖 Model Used

This project uses a free OpenRouter model (for example: mistralai/mistral-7b-instruct or similar).

Why OpenRouter:

Free tier available

No OpenAI API required

Supports long-form generation

Simple HTTP API

🧠 Approach

PDF Upload & Text Extraction

PDFs are uploaded through Streamlit

Text is extracted using pdfplumber

Mock RAG (Retrieval-Augmented Generation)

Extracted PDF text is used as context

This context is injected directly into the LLM prompt

Handbook Generation

User asks for a handbook

The system sends a structured prompt with PDF content

The LLM generates long-form structured text

Token Limit Handling

Uses small max_tokens (e.g., 600)

Prevents free-tier credit errors

📈 Future Improvements

Planned enhancements:

Chunking for Long Documents
Split PDF text into chunks and generate the handbook section-by-section to reach 20,000+ words.

Downloadable Output
Export the handbook as .txt, .md, or .pdf.

Progress Indicator
Show progress while generating long handbooks.

True RAG Integration
Replace mock RAG with:

Vector database (Supabase / pgvector)

LightRAG knowledge graph

📹 Demo

The demo shows:
There are screenshots
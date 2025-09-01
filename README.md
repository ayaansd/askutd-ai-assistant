🎓 AskUTD is a lightweight, end-to-end RAG (Retrieval-Augmented Generation) chatbot that helps students quickly find answers to questions about UT Dallas resources and policies (e.g., ISSO CPT/OPT, academic calendar, registrar deadlines).

Built to be developer-friendly and run on free-tier environments (≤8 GB RAM), the project showcases a practical example of combining FastAPI, LangChain, FAISS, and React into a working AI assistant

🚀 What It Solves

❌ Problem: UTD resources are scattered across multiple pages (ISSO, Registrar, Housing, etc.), and finding reliable information is slow.

✅ Solution: Centralize this information into an AI-powered assistant:

Lets students ask natural language questions.

Answers based on curated UTD text snippets (not random web content).

Provides citations to original sources for transparency.

🛠️ Architecture & Flow
flowchart TD
  subgraph Frontend [Frontend – React (CDN)]
    UI[Input box + Ask button]
    OUT[Answer + Sources display]
  end

  subgraph Backend [Backend – FastAPI + LangChain]
    A[FastAPI REST API]
    E[Embedding Builder (FAISS)]
    Q[Q&A Bot – Retriever + LLM]
  end

  subgraph Data [Local Data Sources]
    D1[ISSO CPT/OPT Notes]
    D2[Academic Calendar]
    D3[Registrar FAQs]
  end

  UI -->|POST /ask| A --> Q
  A -->|POST /embed| E
  E --> D1 & D2 & D3
  Q --> OUT

Flow

Text snippets from UTD pages are stored in /backend/data/*.txt.

embed_docs.py builds a FAISS index from those documents.

When a question comes in (POST /ask), the retriever pulls the most relevant chunks.

The LLM (gpt-4o-mini by default) generates an answer grounded in those chunks.

The frontend displays both the answer and source file names.

📊 Data Sources

ISSO CPT/OPT Guidelines → eligibility & process

UTD Academic Calendar → semester dates, census, withdrawals

Registrar FAQs → enrollment, transcripts, graduation

(Extendable) → Housing policies, Health Center resources, Career Center tips

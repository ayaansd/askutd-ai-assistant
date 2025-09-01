import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()
VSTORE_DIR = Path(__file__).parent / "vector_store"

def get_retriever(k: int = 4):
    embed_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embed_model)
    vdb = FAISS.load_local(str(VSTORE_DIR), embeddings, allow_dangerous_deserialization=True)
    return vdb.as_retriever(search_kwargs={"k": k})

def ask_llm(question: str) -> dict:
    retriever = get_retriever()
    # manual retrieve + simple join to keep it explicit
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])
    sources = list({d.metadata.get("source", "unknown") for d in docs})

    llm_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=llm_model, temperature=0.1)

    prompt = (
        "You are a helpful assistant answering questions about UTD policies and resources. "
        "Use ONLY the provided context. If the answer is not in the context, say you don't know "
        "and suggest where to find it on UTD sites.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer succinctly and cite the source file names if applicable."
    )
    resp = llm.invoke(prompt)
    return {"answer": resp.content, "sources": sources}

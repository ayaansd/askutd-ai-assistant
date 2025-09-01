import os
from dotenv import load_dotenv
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from load_data import load_txt_files, chunk_docs

load_dotenv()

VSTORE_DIR = Path(__file__).parent / "vector_store"

def main():
    docs = load_txt_files()
    if not docs:
        raise SystemExit("No .txt files in /backend/data. Add content then rerun.")

    chunks = chunk_docs(docs)
    embed_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embed_model)

    vdb = FAISS.from_documents(chunks, embeddings)
    VSTORE_DIR.mkdir(exist_ok=True)
    vdb.save_local(str(VSTORE_DIR))
    print(f"✅ FAISS index saved to {VSTORE_DIR} (chunks: {len(chunks)})")

if __name__ == "__main__":
    main()

from pathlib import Path
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

DATA_DIR = Path(__file__).parent / "data"

def load_txt_files() -> List[Document]:
    docs: List[Document] = []
    for p in sorted(DATA_DIR.glob("*.txt")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        docs.append(Document(page_content=text, metadata={"source": p.name}))
    return docs

def chunk_docs(docs: List[Document], chunk_size=900, chunk_overlap=120) -> List[Document]:
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

if __name__ == "__main__":
    raw = load_txt_files()
    chunks = chunk_docs(raw)
    print(f"Loaded {len(raw)} files → {len(chunks)} chunks")

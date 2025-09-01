import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from embed_docs import main as embed_main
from qa_bot import ask_llm

load_dotenv()

app = FastAPI(title="AskUTD API", version="0.1.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskBody(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/embed")
def embed():
    try:
        embed_main()
        return {"status": "ok", "message": "Index rebuilt"}
    except SystemExit as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask")
def ask(body: AskBody):
    q = (body.query or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty query")
    try:
        res = ask_llm(q)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

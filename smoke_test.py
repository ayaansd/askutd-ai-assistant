import os
import json
import pytest
from fastapi.testclient import TestClient
import app

client = TestClient(app.app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_embed_and_ask_monkeypatched(monkeypatch):
    # avoid real OpenAI calls in CI smoke: stub ask_llm
    from app import ask_llm
    def fake_ask_llm(q: str):
        return {"answer": "This is a stub answer for: " + q, "sources": ["isso_cpt.sample.txt"]}
    monkeypatch.setattr("app.ask_llm", fake_ask_llm)

    # embed endpoint may fail if no data; ensure sample exists
    r = client.post("/embed")
    # embed may raise if no OPENAI key; tolerate 400 here
    assert r.status_code in (200, 400)

    r2 = client.post("/ask", json={"query": "What is CPT?"})
    assert r2.status_code == 200
    j = r2.json()
    assert "answer" in j and "sources" in j

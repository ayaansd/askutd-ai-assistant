#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python embed_docs.py || true
uvicorn app:app --reload --port 8000

#!/usr/bin/env bash
set -e
echo "== Backend =="
pushd backend >/dev/null
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env || true
python embed_docs.py || true
uvicorn app:app --reload --port 8000 &
BACK_PID=$!
popd >/dev/null

echo "== Frontend =="
python -m http.server 5173 &
FRONT_PID=$!

echo "Open http://localhost:5173/frontend in your browser."
echo "Press Ctrl+C to stop."
wait $BACK_PID $FRONT_PID || true

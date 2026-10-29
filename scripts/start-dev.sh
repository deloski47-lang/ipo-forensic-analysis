#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cd "$ROOT/frontend"
npm install
cd "$ROOT"
trap 'kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true' EXIT INT TERM
(cd "$ROOT/backend" && "$ROOT/backend/.venv/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8000) &
BACKEND_PID=$!
(cd "$ROOT/frontend" && npm run dev) &
FRONTEND_PID=$!
echo "Frontend: http://127.0.0.1:5173"
echo "API docs:  http://127.0.0.1:8000/docs"
wait

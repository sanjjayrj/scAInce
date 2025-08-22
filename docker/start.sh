#!/usr/bin/env bash
set -euo pipefail

: "${API_PORT:=8000}"
: "${WEB_PORT:=3000}"

: "${API_MODULE:=python.app:app}"

echo "[start] FastAPI -> ${API_MODULE} on :${API_PORT}"
uvicorn "${API_MODULE}" --host 0.0.0.0 --port "${API_PORT}" &

echo "[start] Next.js on :${WEB_PORT}"
cd /app/frontend

if [ -f ".next/standalone/server.js" ]; then
  node .next/standalone/server.js -p "${WEB_PORT}"
else
  node node_modules/next/dist/bin/next start -p "${WEB_PORT}"
fi

wait -n

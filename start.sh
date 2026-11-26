#!/usr/bin/env bash
set -euo pipefail

# Evitar levantar una segunda instancia si el puerto 8000 ya responde
if curl -sf http://127.0.0.1:8000/health >/dev/null 2>&1; then
  exit 0
fi

ROOT_DIR="/mnt/storage/Projects/stream/local-stream-deck"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_PYTHON="$BACKEND_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Error: No se encontró el entorno virtual en $VENV_PYTHON" >&2
  exit 1
fi

cd "$BACKEND_DIR"
exec "$VENV_PYTHON" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
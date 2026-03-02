#!/bin/bash
# feature/multimodal-rag ブランチ用停止スクリプト

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ports.env"

echo "=== Multimodal RAG サーバー停止 ==="

# バックエンド停止
BACKEND_PIDS=$(lsof -ti:"$BACKEND_PORT" 2>/dev/null || true)
if [ -n "$BACKEND_PIDS" ]; then
  echo "$BACKEND_PIDS" | xargs kill 2>/dev/null || true
  echo "Backend (port $BACKEND_PORT) 停止"
else
  echo "Backend (port $BACKEND_PORT) は起動していません"
fi

# フロントエンド停止
FRONTEND_PIDS=$(lsof -ti:"$FRONTEND_PORT" 2>/dev/null || true)
if [ -n "$FRONTEND_PIDS" ]; then
  echo "$FRONTEND_PIDS" | xargs kill 2>/dev/null || true
  echo "Frontend (port $FRONTEND_PORT) 停止"
else
  echo "Frontend (port $FRONTEND_PORT) は起動していません"
fi

echo "完了"

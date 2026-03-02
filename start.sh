#!/bin/bash
# feature/multimodal-rag ブランチ用起動スクリプト
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ports.env"

LOG_DIR="$SCRIPT_DIR/data/logs"
mkdir -p "$LOG_DIR"

echo "=== Multimodal RAG サーバー起動 ==="
echo "Backend: http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"

# バックエンド起動
cd "$SCRIPT_DIR/backend"
.venv/bin/uvicorn app.main:app --reload --port "$BACKEND_PORT" \
  > "$LOG_DIR/backend.log" 2>&1 &
echo "Backend PID: $!"

# フロントエンド起動
cd "$SCRIPT_DIR/frontend"
NEXT_PUBLIC_API_URL="http://localhost:$BACKEND_PORT" \
  npx next dev --port "$FRONTEND_PORT" \
  > "$LOG_DIR/frontend.log" 2>&1 &
echo "Frontend PID: $!"

echo ""
echo "ログ確認:"
echo "  tail -f $LOG_DIR/backend.log"
echo "  tail -f $LOG_DIR/frontend.log"
echo ""
echo "停止: ./stop.sh"

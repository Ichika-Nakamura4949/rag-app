#!/bin/bash
set -e

cd "$(dirname "$0")"

# ポート設定を読み込む
source ports.env

# 既にそのポートで動いているプロセスがあれば停止
lsof -ti:$BACKEND_PORT  | xargs kill 2>/dev/null || true
lsof -ti:$FRONTEND_PORT | xargs kill 2>/dev/null || true

sleep 1

# Next.jsのロックファイルを削除（ブランチ切替時に残ることがある）
rm -f frontend/.next/dev/lock

# --- backend/.env を自動生成 ---
# OPENAI_API_KEY は既存の .env から引き継ぐ
EXISTING_OPENAI_KEY=""
if [ -f backend/.env ]; then
  EXISTING_OPENAI_KEY=$(grep '^OPENAI_API_KEY=' backend/.env | cut -d'=' -f2- || true)
fi

cat > backend/.env <<EOF
OPENAI_API_KEY=${EXISTING_OPENAI_KEY}
UPLOAD_DIR=./data/uploads
FRONTEND_URL=http://localhost:${FRONTEND_PORT}
EOF
echo "backend/.env を生成しました (FRONTEND_URL=http://localhost:${FRONTEND_PORT})"

# フロントエンドの接続先を更新
echo "NEXT_PUBLIC_API_URL=http://localhost:$BACKEND_PORT" > frontend/.env.local

# ログディレクトリ作成
mkdir -p data/logs

# バックエンド起動
cd backend
.venv/bin/uvicorn app.main:app --reload --port $BACKEND_PORT > ../data/logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# フロントエンド起動
cd frontend
npx next dev --port $FRONTEND_PORT > ../data/logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

echo "==================================="
echo "  Branch:    $BRANCH"
echo "  Backend:   http://localhost:$BACKEND_PORT  (PID: $BACKEND_PID)"
echo "  Frontend:  http://localhost:$FRONTEND_PORT  (PID: $FRONTEND_PID)"
echo "==================================="
echo ""
echo "ログを見るには:"
echo "  tail -f data/logs/backend.log"
echo "  tail -f data/logs/frontend.log"
echo ""
echo "停止するには:"
echo "  ./stop.sh"

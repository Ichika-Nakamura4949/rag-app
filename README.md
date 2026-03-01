# 社内ナレッジ Q&A RAGアプリ

社内ドキュメント（PDF・DOCX・TXT）をアップロードし、RAG（Retrieval-Augmented Generation）を用いてAIがドキュメントの内容に基づいて質問に回答するWebアプリケーションです。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python 3.12 + FastAPI |
| RAGフレームワーク | LangChain |
| ベクトルDB | ChromaDB（ローカル） |
| Embedding | OpenAI text-embedding-3-small |
| LLM | GPT-4o (OpenAI API) |
| フロントエンド | Next.js (React) + Tailwind CSS |

## セットアップ

### 前提条件

- Python 3.12+
- Node.js 18+
- OpenAI APIキー

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd rag-app
```

### 2. バックエンドのセットアップ

```bash
cd backend
pip install -r requirements.txt
```

環境変数を設定します：

```bash
cp .env.example .env
```

`.env` を編集し、OpenAI APIキーを設定してください：

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. フロントエンドのセットアップ

```bash
cd frontend
npm install
```

## 起動方法

ターミナルを2つ開き、それぞれで起動します。

### バックエンド（ポート3003）

```bash
cd backend
uvicorn app.main:app --reload --port 3003
```

### フロントエンド（ポート3002）

```bash
cd frontend
npm run dev
```

### アクセス

- **チャット画面**: http://localhost:3002
- **ドキュメント管理**: http://localhost:3002/documents

## 使い方

### 1. ドキュメントをアップロード

http://localhost:3002/documents にアクセスし、PDF・DOCX・TXTファイルをドラッグ＆ドロップ（またはクリックして選択）でアップロードします。

### 2. 質問する

http://localhost:3002 のチャット画面で質問を入力すると、アップロードしたドキュメントの内容に基づいてAIが回答します。回答には参照元ドキュメントの情報も表示されます。

## 環境変数

### バックエンド（`backend/.env`）

| 変数名 | 説明 | デフォルト値 |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI APIキー（必須） | - |
| `CHROMA_PERSIST_DIR` | ChromaDBデータ保存先 | `./data/chroma` |
| `UPLOAD_DIR` | アップロードファイル保存先 | `./data/uploads` |

### フロントエンド（`frontend/.env.local`）

| 変数名 | 説明 | デフォルト値 |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | バックエンドAPIのURL | `http://localhost:3003` |

## 開発コマンド

### バックエンド

```bash
cd backend

# テスト
pytest

# リント
ruff check .

# フォーマット
ruff format .
```

### フロントエンド

```bash
cd frontend

# ビルド
npm run build

# リント
npm run lint
```

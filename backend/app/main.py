"""FastAPIアプリケーション エントリポイント."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, documents


def create_app() -> FastAPI:
    """FastAPIアプリケーションを生成."""
    application = FastAPI(
        title="社内ナレッジQ&A RAGアプリ",
        description="社内ドキュメントに基づいてAIが質問に回答するAPIサーバー",
        version="0.1.0",
    )

    # CORS設定（フロントエンド開発用）
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3002"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ルーター登録
    application.include_router(chat.router)
    application.include_router(documents.router)

    @application.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

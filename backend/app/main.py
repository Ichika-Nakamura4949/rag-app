"""FastAPIアプリケーション エントリポイント."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import chat, documents
from app.core.config import get_settings


def create_app() -> FastAPI:
    """FastAPIアプリケーションを生成."""
    settings = get_settings()

    application = FastAPI(
        title="社内ナレッジQ&A RAGアプリ",
        description="社内ドキュメントに基づいてAIが質問に回答するAPIサーバー",
        version="0.1.0",
    )

    # CORS設定（フロントエンド開発用）
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ルーター登録
    application.include_router(chat.router)
    application.include_router(documents.router)

    # 画像ファイル配信用の静的ファイルマウント
    application.mount(
        "/images",
        StaticFiles(directory=str(settings.image_path)),
        name="images",
    )

    @application.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()

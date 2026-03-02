"""アプリケーション設定管理."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """環境変数から読み込むアプリケーション設定."""

    openai_api_key: str = ""
    chroma_persist_dir: str = "./data/chroma"
    upload_dir: str = "./data/uploads"

    # RAG設定
    chunk_size: int = 800
    chunk_overlap: int = 200
    retriever_k: int = 8

    # OpenAIモデル設定
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o"

    # 画像抽出設定
    image_dir: str = "./data/images"
    min_image_width: int = 100
    min_image_height: int = 100
    caption_model: str = "gpt-4o-mini"

    # CORS設定
    frontend_url: str = "http://localhost:3002"

    # ファイルアップロード制限
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set[str] = {".pdf", ".docx"}

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def chroma_persist_path(self) -> Path:
        """ChromaDB永続化ディレクトリのPathオブジェクト."""
        path = Path(self.chroma_persist_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def image_path(self) -> Path:
        """画像保存ディレクトリのPathオブジェクト."""
        path = Path(self.image_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def upload_path(self) -> Path:
        """アップロードディレクトリのPathオブジェクト."""
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    """設定シングルトンを取得."""
    return Settings()

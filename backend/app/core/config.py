"""アプリケーション設定管理."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """環境変数から読み込むアプリケーション設定."""

    openai_api_key: str = ""
    upload_dir: str = "./data/uploads"

    # OpenAI File Search設定
    vector_store_id: str = ""
    file_search_max_results: int = 8

    # OpenAIモデル設定
    llm_model: str = "gpt-4o"

    # ファイルアップロード制限
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set[str] = {".pdf", ".docx"}

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

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

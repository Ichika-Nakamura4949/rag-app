"""OpenAI File Search用ドキュメント取り込みパイプライン."""

import logging
from pathlib import Path

from openai import OpenAI

from app.core.config import Settings

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """ファイルをOpenAI Files APIにアップロードし、Vector Storeに追加."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._vector_store_id = settings.vector_store_id

    def ensure_vector_store(self) -> str:
        """ベクトルストアが存在しなければ作成し、IDを返す."""
        if self._vector_store_id:
            return self._vector_store_id

        vector_store = self._client.vector_stores.create(
            name="rag-app-knowledge-base",
        )
        self._vector_store_id = vector_store.id
        logger.info("Vector Store created: %s", vector_store.id)
        return vector_store.id

    @property
    def vector_store_id(self) -> str:
        """現在のベクトルストアIDを取得."""
        return self._vector_store_id

    def ingest(self, file_path: Path, document_id: str, filename: str) -> str:
        """ファイルをOpenAIにアップロードし、Vector Storeに追加.

        Args:
            file_path: ドキュメントファイルのパス
            document_id: ドキュメントの一意ID
            filename: 元のファイル名

        Returns:
            OpenAIのfile_id
        """
        vs_id = self.ensure_vector_store()

        # OpenAI Files APIにアップロード
        with open(file_path, "rb") as f:
            uploaded_file = self._client.files.create(
                file=f,
                purpose="assistants",
            )
        logger.info("File uploaded: %s (%s)", uploaded_file.id, filename)

        # Vector Storeに追加（処理完了まで待機）
        self._client.vector_stores.files.create_and_poll(
            vector_store_id=vs_id,
            file_id=uploaded_file.id,
        )
        logger.info("File added to vector store: %s", uploaded_file.id)

        return uploaded_file.id

    def delete_by_document_id(self, openai_file_id: str) -> None:
        """OpenAI上のファイルをVector StoreとFiles APIから削除."""
        if not openai_file_id:
            return

        vs_id = self._vector_store_id
        if vs_id:
            try:
                self._client.vector_stores.files.delete(
                    vector_store_id=vs_id,
                    file_id=openai_file_id,
                )
            except Exception:
                logger.warning(
                    "Failed to remove file %s from vector store", openai_file_id
                )

        try:
            self._client.files.delete(file_id=openai_file_id)
        except Exception:
            logger.warning("Failed to delete file %s", openai_file_id)

"""ドキュメントファイル管理サービス."""

import json
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import Settings
from app.models.schemas import DocumentMetadata


class DocumentService:
    """ファイル保存・メタデータ管理."""

    def __init__(self, settings: Settings) -> None:
        self._upload_dir = settings.upload_path
        self._metadata_path = self._upload_dir / "_metadata.json"
        self._metadata: dict[str, dict] = self._load_metadata()

    def _load_metadata(self) -> dict[str, dict]:
        """メタデータファイルを読み込む."""
        if self._metadata_path.exists():
            return json.loads(self._metadata_path.read_text(encoding="utf-8"))
        return {}

    def _save_metadata(self) -> None:
        """メタデータファイルを保存."""
        self._metadata_path.write_text(
            json.dumps(self._metadata, ensure_ascii=False, default=str, indent=2),
            encoding="utf-8",
        )

    async def save_file(self, file: UploadFile) -> DocumentMetadata:
        """アップロードファイルを保存しメタデータを記録."""
        document_id = uuid.uuid4().hex
        filename = file.filename or "unknown"
        suffix = Path(filename).suffix

        save_path = self._upload_dir / f"{document_id}{suffix}"
        content = await file.read()
        save_path.write_bytes(content)

        metadata = DocumentMetadata(
            document_id=document_id,
            filename=filename,
            file_size=len(content),
            content_type=file.content_type or "application/octet-stream",
        )
        self._metadata[document_id] = metadata.model_dump()
        self._save_metadata()
        return metadata

    def update_openai_file_id(self, document_id: str, openai_file_id: str) -> None:
        """Ingestion後にOpenAIファイルIDを更新."""
        if document_id in self._metadata:
            self._metadata[document_id]["openai_file_id"] = openai_file_id
            self._save_metadata()

    def list_documents(self) -> list[DocumentMetadata]:
        """全ドキュメントのメタデータ一覧を取得."""
        return [DocumentMetadata(**meta) for meta in self._metadata.values()]

    def get_document(self, document_id: str) -> DocumentMetadata | None:
        """指定IDのドキュメントメタデータを取得."""
        if document_id in self._metadata:
            return DocumentMetadata(**self._metadata[document_id])
        return None

    def get_file_path(self, document_id: str) -> Path | None:
        """ドキュメントIDに対応するファイルパスを取得."""
        meta = self._metadata.get(document_id)
        if not meta:
            return None
        suffix = Path(meta["filename"]).suffix
        path = self._upload_dir / f"{document_id}{suffix}"
        return path if path.exists() else None

    def delete_file(self, document_id: str) -> bool:
        """ファイルとメタデータを削除."""
        file_path = self.get_file_path(document_id)
        if file_path and file_path.exists():
            file_path.unlink()

        if document_id in self._metadata:
            del self._metadata[document_id]
            self._save_metadata()
            return True
        return False

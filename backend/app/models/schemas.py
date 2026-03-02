"""Pydanticリクエスト/レスポンスモデル."""

from datetime import datetime

from pydantic import BaseModel, Field

# --- Chat ---

# BaseModelを引数に取ることでpydanticの便利な機能を使うことのできるクラスになる
class ChatRequest(BaseModel):
    """チャットリクエスト."""

    question: str = Field(..., min_length=1, description="ユーザーの質問")


class SourceDocument(BaseModel):
    """参照元ドキュメント情報."""

    document_name: str
    page_content: str
    image_url: str | None = None
    metadata: dict = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """チャットレスポンス."""

    answer: str
    source_documents: list[SourceDocument] = Field(default_factory=list)


# --- Documents ---


class DocumentMetadata(BaseModel):
    """ドキュメントメタデータ."""

    document_id: str
    filename: str
    file_size: int
    content_type: str
    chunk_count: int = 0
    image_count: int = 0
    uploaded_at: datetime = Field(default_factory=datetime.now)


class DocumentUploadResponse(BaseModel):
    """アップロードレスポンス."""

    document_id: str
    filename: str
    chunk_count: int
    image_count: int = 0
    message: str = "ドキュメントのアップロードと処理が完了しました"


class DocumentListResponse(BaseModel):
    """ドキュメント一覧レスポンス."""

    documents: list[DocumentMetadata]
    total: int


class DeleteResponse(BaseModel):
    """削除レスポンス."""

    message: str
    document_id: str

"""ドキュメント管理APIルート."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.api.deps import DocumentServiceDep, IngestionDep, SettingsDep
from app.models.schemas import (
    DeleteResponse,
    DocumentListResponse,
    DocumentUploadResponse,
)

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile,
    settings: SettingsDep,
    doc_service: DocumentServiceDep,
    ingestion: IngestionDep,
) -> DocumentUploadResponse:
    """ドキュメントをアップロードし、OpenAI File Searchで処理."""
    # ファイル形式バリデーション
    filename = file.filename or ""
    suffix = Path(filename).suffix.lower()
    if suffix not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "サポートされていないファイル形式です。"
                f"許可: {', '.join(settings.allowed_extensions)}"
            ),
        )

    # ファイルサイズバリデーション
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=(
                "ファイルサイズが上限"
                f"({settings.max_file_size // (1024 * 1024)}MB)"
                "を超えています"
            ),
        )
    await file.seek(0)

    # ファイル保存
    metadata = await doc_service.save_file(file)

    # OpenAI Files API + Vector Storeにアップロード
    file_path = doc_service.get_file_path(metadata.document_id)
    if not file_path:
        raise HTTPException(status_code=500, detail="ファイルの保存に失敗しました")

    openai_file_id = ingestion.ingest(
        file_path=file_path,
        document_id=metadata.document_id,
        filename=metadata.filename,
    )
    doc_service.update_openai_file_id(metadata.document_id, openai_file_id)

    return DocumentUploadResponse(
        document_id=metadata.document_id,
        filename=metadata.filename,
        openai_file_id=openai_file_id,
    )


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    doc_service: DocumentServiceDep,
) -> DocumentListResponse:
    """アップロード済みドキュメント一覧を取得."""
    documents = doc_service.list_documents()
    return DocumentListResponse(documents=documents, total=len(documents))


@router.delete("/{document_id}", response_model=DeleteResponse)
async def delete_document(
    document_id: str,
    doc_service: DocumentServiceDep,
    ingestion: IngestionDep,
) -> DeleteResponse:
    """ドキュメントを削除（ローカルファイル + OpenAI）."""
    doc = doc_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="ドキュメントが見つかりません")

    # OpenAIからファイルを削除
    ingestion.delete_by_document_id(doc.openai_file_id)

    # ローカルファイルとメタデータを削除
    doc_service.delete_file(document_id)

    return DeleteResponse(
        message="ドキュメントを削除しました",
        document_id=document_id,
    )

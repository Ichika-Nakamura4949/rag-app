"""依存性注入."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.rag.chain import RAGChain
from app.core.rag.ingestion import IngestionPipeline
from app.services.document_service import DocumentService


@lru_cache
def get_document_service() -> DocumentService:
    """DocumentServiceシングルトンを取得."""
    return DocumentService(get_settings())


@lru_cache
def get_ingestion_pipeline() -> IngestionPipeline:
    """IngestionPipelineシングルトンを取得."""
    return IngestionPipeline(get_settings())


@lru_cache
def get_rag_chain() -> RAGChain:
    """RAGChainシングルトンを取得."""
    return RAGChain(get_settings())


# Annotated型エイリアス
SettingsDep = Annotated[Settings, Depends(get_settings)]
DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
IngestionDep = Annotated[IngestionPipeline, Depends(get_ingestion_pipeline)]
RAGChainDep = Annotated[RAGChain, Depends(get_rag_chain)]

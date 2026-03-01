"""ドキュメント取り込みパイプライン."""

from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings


class IngestionPipeline:
    """PDF/DOCX解析 → チャンク分割 → Embedding → ChromaDB保存."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        self._client = chromadb.PersistentClient(
            path=str(settings.chroma_persist_path),
        )

    def _parse_pdf(self, file_path: Path) -> str:
        """PDFファイルからテキストを抽出."""
        import pymupdf

        doc = pymupdf.open(str(file_path))
        pages: list[str] = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                pages.append(text)
        doc.close()
        return "\n\n".join(pages)

    def _parse_docx(self, file_path: Path) -> str:
        """DOCXファイルからテキストを抽出."""
        from docx import Document as DocxDocument

        doc = DocxDocument(str(file_path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)

    def _parse_file(self, file_path: Path) -> str:
        """ファイル形式に応じてテキストを抽出."""
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return self._parse_pdf(file_path)
        if suffix == ".docx":
            return self._parse_docx(file_path)
        raise ValueError(f"サポートされていないファイル形式: {suffix}")

    def ingest(self, file_path: Path, document_id: str, filename: str) -> int:
        """ドキュメントを解析してChromaDBに保存.

        Args:
            file_path: ドキュメントファイルのパス
            document_id: ドキュメントの一意ID
            filename: 元のファイル名

        Returns:
            生成されたチャンク数
        """
        text = self._parse_file(file_path)
        if not text.strip():
            return 0

        chunks = self._splitter.split_text(text)
        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]

        vectorstore = Chroma(
            client=self._client,
            collection_name="documents",
            embedding_function=self._embeddings,
        )
        vectorstore.add_documents(documents)

        return len(documents)

    def delete_by_document_id(self, document_id: str) -> None:
        """指定ドキュメントIDのチャンクをChromaDBから削除."""
        collection = self._client.get_or_create_collection("documents")
        collection.delete(where={"document_id": document_id})

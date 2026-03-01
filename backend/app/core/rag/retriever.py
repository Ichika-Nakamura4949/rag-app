"""ChromaDBベクトル検索."""

import chromadb
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

from app.core.config import Settings


class RetrieverFactory:
    """ChromaDBからLangChain Retrieverを生成."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )
        self._client = chromadb.PersistentClient(
            path=str(settings.chroma_persist_path),
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """ベクトル検索Retrieverを取得."""
        vectorstore = Chroma(
            client=self._client,
            collection_name="documents",
            embedding_function=self._embeddings,
        )
        return vectorstore.as_retriever(
            search_kwargs={"k": self._settings.retriever_k},
        )

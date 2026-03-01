"""OpenAI Responses API（file_search）によるRAGチェーン."""

import logging

from openai import OpenAI

from app.core.config import Settings
from app.core.rag.ingestion import IngestionPipeline
from app.models.schemas import ChatResponse, SourceDocument

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
あなたは社内ドキュメントに基づいて質問に回答するアシスタントです。

以下のルールに従ってください：
- 提供されたコンテキスト（検索結果）の情報のみに基づいて回答してください。
- コンテキストに答えが見つからない場合は、\
「提供されたドキュメントからは該当する情報が見つかりませんでした。」\
と回答してください。
- 回答は簡潔かつ正確にしてください。
- 日本語で回答してください。
"""


class RAGChain:
    """OpenAI Responses APIを使ったRAG質問応答チェーン."""

    def __init__(
        self, settings: Settings, ingestion: IngestionPipeline
    ) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._ingestion = ingestion
        self._model = settings.llm_model
        self._max_results = settings.file_search_max_results

    def invoke(self, question: str) -> ChatResponse:
        """質問に対してFile Searchを使い回答を生成.

        Args:
            question: ユーザーの質問文

        Returns:
            回答と参照元ドキュメント情報
        """
        vector_store_id = self._ingestion.vector_store_id
        if not vector_store_id:
            return ChatResponse(
                answer="ドキュメントがまだアップロードされていません。",
                source_documents=[],
            )

        response = self._client.responses.create(
            model=self._model,
            instructions=SYSTEM_PROMPT,
            input=question,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store_id],
                    "max_num_results": self._max_results,
                }
            ],
        )

        # レスポンスからテキストとソース情報を抽出
        answer = response.output_text

        source_documents = self._extract_sources(response)

        return ChatResponse(answer=answer, source_documents=source_documents)

    def _extract_sources(self, response: object) -> list[SourceDocument]:
        """レスポンスのアノテーションからソースドキュメント情報を抽出."""
        sources: list[SourceDocument] = []
        seen_file_ids: set[str] = set()

        for item in response.output:
            if item.type != "message":
                continue
            for content in item.content:
                if content.type != "output_text":
                    continue
                for annotation in getattr(content, "annotations", []):
                    if annotation.type != "file_citation":
                        continue
                    file_id = annotation.file_id
                    if file_id in seen_file_ids:
                        continue
                    seen_file_ids.add(file_id)
                    sources.append(
                        SourceDocument(
                            document_name=getattr(
                                annotation, "filename", file_id
                            ),
                            page_content=f"[File Search citation: {file_id}]",
                            metadata={"file_id": file_id},
                        )
                    )

        return sources

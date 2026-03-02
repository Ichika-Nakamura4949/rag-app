"""LangChain RAGチェーン."""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.rag.retriever import RetrieverFactory
from app.models.schemas import ChatResponse, SourceDocument

SYSTEM_PROMPT = """\
あなたは社内ドキュメントに基づいて質問に回答するアシスタントです。

以下のルールに従ってください：
- 提供されたコンテキスト（検索結果）の情報のみに基づいて回答してください。
- コンテキストに答えが見つからない場合は、\
「提供されたドキュメントからは該当する情報が見つかりませんでした。」\
と回答してください。
- 回答は簡潔かつ正確にしてください。
- 日本語で回答してください。

コンテキスト:
{context}
"""


def _format_docs(docs: list[Document]) -> str:
    """検索結果ドキュメントをテキストに変換."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


class RAGChain:
    """RAG質問応答チェーン."""

    def __init__(self, settings: Settings) -> None:
        self._retriever_factory = RetrieverFactory(settings)
        self._llm = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=settings.openai_api_key,
            temperature=0,
        )
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ])

    def _translate_query(self, question: str) -> str:
        """検索精度向上のため、質問を英語に翻訳."""
        translate_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Translate the following user query to English for use as a "
                "search query against English documents. Output ONLY the "
                "translated query, nothing else.",
            ),
            ("human", "{query}"),
        ])
        chain = translate_prompt | self._llm | StrOutputParser()
        return chain.invoke({"query": question})

    def invoke(self, question: str) -> ChatResponse:
        """質問に対してRAGで回答を生成.

        Args:
            question: ユーザーの質問文

        Returns:
            回答と参照元ドキュメント情報
        """
        retriever = self._retriever_factory.get_retriever()

        # 検索精度向上のため質問を英語に翻訳して検索
        search_query = self._translate_query(question)
        retrieved_docs = retriever.invoke(search_query)

        # LCELチェーン: context + question → prompt → LLM → parser
        chain = (
            {
                "context": lambda _: _format_docs(retrieved_docs),
                "question": RunnablePassthrough(),
            }
            | self._prompt
            | self._llm
            | StrOutputParser()
        )

        answer = chain.invoke(question)

        source_documents = []
        for doc in retrieved_docs:
            image_url = None
            if doc.metadata.get("type") == "image_caption":
                image_path = doc.metadata.get("image_path", "")
                if image_path:
                    image_url = f"/images/{image_path}"

            source_documents.append(
                SourceDocument(
                    document_name=doc.metadata.get("filename", "不明"),
                    page_content=doc.page_content[:200],
                    image_url=image_url,
                    metadata=doc.metadata,
                )
            )

        return ChatResponse(answer=answer, source_documents=source_documents)

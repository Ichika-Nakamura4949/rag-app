"""チャットAPIルート."""

from fastapi import APIRouter

from app.api.deps import RAGChainDep
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_chain: RAGChainDep,
) -> ChatResponse:
    """質問を受け取り、RAGで回答を生成."""
    return rag_chain.invoke(request.question)

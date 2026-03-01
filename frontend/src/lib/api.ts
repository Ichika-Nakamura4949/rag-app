import type {
  ChatResponse,
  DocumentUploadResponse,
  DocumentListResponse,
  DeleteResponse,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3003";

export async function sendChatMessage(question: string): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat/`, {

    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "チャットの送信に失敗しました");
  }
  return res.json();
}

export async function uploadDocument(
  file: File,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_URL}/api/documents/`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "ドキュメントのアップロードに失敗しました");
  }
  return res.json();
}

export async function listDocuments(): Promise<DocumentListResponse> {
  const res = await fetch(`${API_URL}/api/documents/`,{
    method:"GET",
  })
  if (!res.ok) {
    throw new Error("ドキュメント一覧の取得に失敗しました");
  }
  return res.json();
}

export async function deleteDocument(
  documentId: string,
): Promise<DeleteResponse> {
  const res = await fetch(`${API_URL}/api/documents/${documentId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "ドキュメントの削除に失敗しました");
  }
  return res.json();
}

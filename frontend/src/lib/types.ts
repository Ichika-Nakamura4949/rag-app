// Chat types
export interface SourceDocument {
  document_name: string;
  page_content: string;
  image_url?: string;
  metadata: Record<string, unknown>;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  source_documents: SourceDocument[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  source_documents?: SourceDocument[];
}

// Document types
export interface DocumentMetadata {
  document_id: string;
  filename: string;
  file_size: number;
  content_type: string;
  chunk_count: number;
  image_count: number;
  uploaded_at: string;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  chunk_count: number;
  image_count: number;
  message: string;
}

export interface DocumentListResponse {
  documents: DocumentMetadata[];
  total: number;
}

export interface DeleteResponse {
  message: string;
  document_id: string;
}

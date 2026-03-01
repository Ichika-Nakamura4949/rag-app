"use client";

import { useState, useEffect, useCallback } from "react";
import type { DocumentMetadata } from "@/lib/types";
import { listDocuments, deleteDocument } from "@/lib/api";
import UploadZone from "@/components/documents/UploadZone";
import DocumentList from "@/components/documents/DocumentList";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listDocuments();
      setDocuments(data.documents);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "ドキュメント一覧の取得に失敗しました",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  async function handleDelete(documentId: string) {
    try {
      await deleteDocument(documentId);
      await fetchDocuments();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "ドキュメントの削除に失敗しました",
      );
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <h2 className="text-lg font-semibold text-gray-800">
          ドキュメント管理
        </h2>
      </div>
      <div className="flex-1 overflow-auto p-4">
        <div className="mx-auto max-w-4xl space-y-6">
          <UploadZone onUploaded={fetchDocuments} />

          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}

          <div className="rounded-lg bg-white shadow-sm ring-1 ring-gray-200">
            {isLoading ? (
              <p className="py-8 text-center text-sm text-gray-400">
                読み込み中...
              </p>
            ) : (
              <DocumentList
                documents={documents}
                onDelete={handleDelete}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

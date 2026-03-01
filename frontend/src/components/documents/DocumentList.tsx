import type { DocumentMetadata } from "@/lib/types";

interface DocumentListProps {
  documents: DocumentMetadata[];
  onDelete: (documentId: string) => void;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(isoString: string): string {
  return new Date(isoString).toLocaleString("ja-JP");
}

export default function DocumentList({
  documents,
  onDelete,
}: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-gray-400">
        ドキュメントがありません
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-gray-200 text-xs font-medium uppercase text-gray-500">
            <th className="px-4 py-3">ファイル名</th>
            <th className="px-4 py-3">サイズ</th>
            <th className="px-4 py-3">チャンク数</th>
            <th className="px-4 py-3">アップロード日時</th>
            <th className="px-4 py-3" />
          </tr>
        </thead>
        <tbody>
          {documents.map((doc) => (
            <tr
              key={doc.document_id}
              className="border-b border-gray-100 hover:bg-gray-50"
            >
              <td className="px-4 py-3 font-medium text-gray-800">
                {doc.filename}
              </td>
              <td className="px-4 py-3 text-gray-600">
                {formatFileSize(doc.file_size)}
              </td>
              <td className="px-4 py-3 text-gray-600">{doc.chunk_count}</td>
              <td className="px-4 py-3 text-gray-600">
                {formatDate(doc.uploaded_at)}
              </td>
              <td className="px-4 py-3">
                <button
                  onClick={() => {
                    if (window.confirm(`「${doc.filename}」を削除しますか？`)) {
                      onDelete(doc.document_id);
                    }
                  }}
                  className="text-sm text-red-600 hover:text-red-800"
                >
                  削除
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

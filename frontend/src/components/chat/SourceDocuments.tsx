import type { SourceDocument } from "@/lib/types";

interface SourceDocumentsProps {
  sources: SourceDocument[];
}

export default function SourceDocuments({ sources }: SourceDocumentsProps) {
  if (sources.length === 0) return null;

  return (
    <div className="mt-2">
      <p className="mb-1 text-xs font-medium text-gray-500">参照元ドキュメント:</p>
      <div className="flex flex-col gap-1">
        {sources.map((source, index) => (
          <details
            key={index}
            className="rounded border border-gray-200 bg-gray-50 text-xs"
          >
            <summary className="cursor-pointer px-3 py-1.5 font-medium text-gray-700 hover:bg-gray-100">
              {source.document_name}
            </summary>
            <div className="border-t border-gray-200 px-3 py-2 text-gray-600">
              <p className="whitespace-pre-wrap">{source.page_content}</p>
            </div>
          </details>
        ))}
      </div>
    </div>
  );
}

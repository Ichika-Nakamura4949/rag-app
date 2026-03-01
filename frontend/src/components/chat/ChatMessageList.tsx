"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/lib/types";
import SourceDocuments from "./SourceDocuments";

interface ChatMessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export default function ChatMessageList({
  messages,
  isLoading,
}: ChatMessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center text-gray-400">
        <p>質問を入力してください</p>
      </div>
    );
  }

  return (
    <div className="flex-1 space-y-4 overflow-y-auto px-4 py-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[80%] rounded-lg px-4 py-3 ${
              message.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-800 shadow-sm ring-1 ring-gray-200"
            }`}
          >
            <p className="whitespace-pre-wrap text-sm">{message.content}</p>
            {message.role === "assistant" && message.source_documents && (
              <SourceDocuments sources={message.source_documents} />
            )}
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="flex justify-start">
          <div className="rounded-lg bg-white px-4 py-3 shadow-sm ring-1 ring-gray-200">
            <div className="flex items-center gap-1">
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.3s]" />
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400 [animation-delay:-0.15s]" />
              <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" />
            </div>
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

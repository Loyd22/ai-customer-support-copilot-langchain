/**
 * Message bubble component for chat conversation rendering.
 *
 * Purpose:
 * - Render user and assistant messages in a chat-style layout.
 * - Show plain text for user messages.
 * - Show the structured answer card for assistant messages.
 */

import type { ChatMessage } from "../types/chat";
import type { CopilotViewMode } from "../types/ui";
import AnswerCard from "./AnswerCard";

type MessageBubbleProps = {
  message: ChatMessage;
  viewMode: CopilotViewMode;
};

export default function MessageBubble({ message, viewMode }: MessageBubbleProps) {
  const isAssistant = message.role === "assistant";
  const isUser = message.role === "user";

  /**
   * Render the assistant response card when present.
   */
  function renderAssistantContent() {
    if (message.response) {
      return <AnswerCard response={message.response} viewMode={viewMode} />;
    }

    return (
      <div className="assistant-fallback-card">
        <p className="message-text">{message.content}</p>
      </div>
    );
  }

  return (
    <div
      className={`message-row ${
        isUser ? "message-row-user" : "message-row-assistant"
      }`}
    >
      <div
        className={`message-bubble ${
          isUser ? "user-bubble" : "assistant-bubble"
        }`}
      >
        {isAssistant ? (
          renderAssistantContent()
        ) : (
          <p className="message-text">{message.content}</p>
        )}
      </div>
    </div>
  );
}

/**
 * Message bubble component for chat conversation rendering.
 *
 * This component displays user messages and assistant messages
 * in separate styles. Assistant messages may include a response card.
 */

import type { ChatMessage } from "../types/chat";
import AnswerCard from "./AnswerCard";

type MessageBubbleProps = {
  message: ChatMessage;
};

export default function MessageBubble({ message }: MessageBubbleProps) {
  /**
   * Render the assistant response card when present.
   */
  function renderAssistantContent() {
    if (message.response) {
      return <AnswerCard response={message.response} />;
    }

    return <p>{message.content}</p>;
  }

  return (
    <div className={`message-row ${message.role}`}>
      <div className={`message-bubble ${message.role}`}>
        {message.role === "assistant" ? renderAssistantContent() : <p>{message.content}</p>}
      </div>
    </div>
  );
}
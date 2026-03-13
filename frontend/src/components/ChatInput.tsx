/**
 * Chat input component for submitting user questions.
 *
 * This component manages the local text input and sends the message
 * to the parent component when the form is submitted.
 */

import { useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => Promise<void>;
  isLoading: boolean;
};

export default function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState("");

  /**
   * Handle form submission and send the current message upward.
   */
  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!message.trim() || isLoading) {
      return;
    }

    const currentMessage = message.trim();
    setMessage("");
    await onSend(currentMessage);
  }

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <input
        type="text"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Ask about refund policy, order 1024, ticket T-9001..."
        className="chat-input"
      />
      <button type="submit" disabled={isLoading} className="chat-button">
        {isLoading ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
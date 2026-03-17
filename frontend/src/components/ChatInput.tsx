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
  const isSubmitDisabled = isLoading || !message.trim();
  const placeholderText = isLoading
    ? "Support Assistant is replying..."
    : "Ask about refunds, orders, tickets, or support policies...";

  /**
   * Handle form submission and send the current message upward.
   */
  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (isSubmitDisabled) {
      return;
    }

    const currentMessage = message.trim();
    setMessage("");
    await onSend(currentMessage);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={`chat-input-form ${isLoading ? "chat-input-form-loading" : ""}`}
      aria-busy={isLoading}
    >
      <input
        type="text"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder={placeholderText}
        className="chat-input"
        aria-label="Message the support assistant"
        autoComplete="off"
        disabled={isLoading}
      />
      <button type="submit" disabled={isSubmitDisabled} className="chat-button">
        {isLoading && <span className="chat-button-spinner" aria-hidden="true" />}
        <span>{isLoading ? "Waiting..." : "Send"}</span>
      </button>
    </form>
  );
}

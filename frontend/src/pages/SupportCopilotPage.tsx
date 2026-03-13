/**
 * Main support copilot page for the frontend.
 *
 * This page manages chat state, sends messages to the backend,
 * and renders the conversation UI.
 */

import { useMemo, useState } from "react";
import { sendChatMessage } from "../api/chat";
import ChatInput from "../components/ChatInput";
import MessageBubble from "../components/MessageBubble";
import type { ChatMessage } from "../types/chat";

export default function SupportCopilotPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sessionId = useMemo(() => {
    /**
     * Create a stable session ID for the current browser tab.
     */
    const existing = sessionStorage.getItem("support_session_id");
    if (existing) {
      return existing;
    }

    const newSessionId = `session_${crypto.randomUUID()}`;
    sessionStorage.setItem("support_session_id", newSessionId);
    return newSessionId;
  }, []);

  /**
   * Send a user message to the backend and append both user and assistant
   * messages to the chat state.
   */
  async function handleSend(message: string): Promise<void> {
    setIsLoading(true);

    const userMessage: ChatMessage = {
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await sendChatMessage({
        session_id: sessionId,
        message,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.answer,
        response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: "Something went wrong while contacting the backend.",
      };

      setMessages((prev) => [...prev, assistantMessage]);
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="container">
        <header className="page-header">
          <h1>AI Customer Support Copilot</h1>
          <p>RAG, memory, tools, routing, escalation, and LangGraph</p>
        </header>

        <section className="chat-window">
          {messages.length === 0 ? (
            <div className="empty-state">
              <p>Try asking:</p>
              <ul>
                <li>What is the refund policy?</li>
                <li>Where is order 1024?</li>
                <li>What is the status of ticket T-9001?</li>
                <li>I think this is fraud and I want a manager.</li>
              </ul>
            </div>
          ) : (
            messages.map((message, index) => (
              <MessageBubble key={`${message.role}-${index}`} message={message} />
            ))
          )}
        </section>

        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    </main>
  );
}
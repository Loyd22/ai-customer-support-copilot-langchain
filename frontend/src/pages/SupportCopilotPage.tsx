/**
 * Main support copilot page for the frontend.
 *
 * Purpose:
 * - Manage chat state and session state.
 * - Send user messages to the backend.
 * - Render the conversation in a cleaner chat-style shell.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage } from "../api/chat";
import ChatInput from "../components/ChatInput";
import MessageBubble from "../components/MessageBubble";
import type { ChatMessage } from "../types/chat";
import type { CopilotViewMode } from "../types/ui";

const SESSION_STORAGE_KEY = "support_session_id";

function createSessionId(): string {
  return `session_${crypto.randomUUID()}`;
}

function getInitialSessionId(): string {
  const existing = sessionStorage.getItem(SESSION_STORAGE_KEY);

  if (existing) {
    return existing;
  }

  const newSessionId = createSessionId();
  sessionStorage.setItem(SESSION_STORAGE_KEY, newSessionId);
  return newSessionId;
}

export default function SupportCopilotPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showTypingIndicator, setShowTypingIndicator] = useState(false);
  const [viewMode, setViewMode] = useState<CopilotViewMode>("user");
  const [sessionId, setSessionId] = useState(getInitialSessionId);
  const [chatStartedAt, setChatStartedAt] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const scrollRafRef = useRef<number | null>(null);

  const shortSessionId = useMemo(
    () => sessionId.replace("session_", "").slice(0, 8).toUpperCase(),
    [sessionId],
  );

  const assistantReplyCount = useMemo(
    () => messages.filter((message) => message.role === "assistant").length,
    [messages],
  );
  const userMessageCount = useMemo(
    () => messages.filter((message) => message.role === "user").length,
    [messages],
  );
  const totalMessageCount = messages.length;

  const sessionStatusLabel = isLoading
    ? "Assistant is replying"
    : totalMessageCount > 0
      ? "Active"
      : "Ready";

  const sessionStatusClass = isLoading
    ? "session-status session-status-busy"
    : "session-status session-status-ready";

  const startedAtLabel = chatStartedAt
    ? new Intl.DateTimeFormat(undefined, {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }).format(chatStartedAt)
    : "Not started";
  const conversationSummary =
    totalMessageCount > 0
      ? `${userMessageCount} from you, ${assistantReplyCount} from assistant`
      : "No messages yet";
  const viewModeDescription =
    viewMode === "developer"
      ? "Developer/Demo View shows action, tools, memory, and raw sources."
      : "User View keeps the chat clean and hides technical details.";

  /**
   * Delay typing indicator slightly to avoid quick flash on fast responses.
   */
  useEffect(() => {
    if (isLoading) {
      const timerId = window.setTimeout(() => {
        setShowTypingIndicator(true);
      }, 170);

      return () => {
        window.clearTimeout(timerId);
      };
    }

    setShowTypingIndicator(false);
    return undefined;
  }, [isLoading]);

  /**
   * Auto-scroll to the newest message with requestAnimationFrame to avoid
   * jumpiness while rows and typing state animate in.
   */
  useEffect(() => {
    if (!messagesEndRef.current) {
      return undefined;
    }

    if (scrollRafRef.current !== null) {
      window.cancelAnimationFrame(scrollRafRef.current);
    }

    const scrollBehavior: ScrollBehavior = messages.length <= 1 ? "auto" : "smooth";

    scrollRafRef.current = window.requestAnimationFrame(() => {
      messagesEndRef.current?.scrollIntoView({
        behavior: scrollBehavior,
        block: "end",
      });
      scrollRafRef.current = null;
    });

    return () => {
      if (scrollRafRef.current !== null) {
        window.cancelAnimationFrame(scrollRafRef.current);
        scrollRafRef.current = null;
      }
    };
  }, [messages.length, isLoading, showTypingIndicator]);

  /**
   * Send a user message to the backend and append both user and assistant
   * messages to the chat state.
   */
  async function handleSend(message: string): Promise<void> {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    setIsLoading(true);

    const userMessage: ChatMessage = {
      role: "user",
      content: trimmedMessage,
    };

    if (messages.length === 0) {
      setChatStartedAt(Date.now());
    }

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await sendChatMessage({
        session_id: sessionId,
        message: trimmedMessage,
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

  /**
   * Reset the active conversation and start a fresh session.
   */
  function handleNewChat() {
    if (isLoading) {
      return;
    }

    const nextSessionId = createSessionId();
    sessionStorage.setItem(SESSION_STORAGE_KEY, nextSessionId);

    setSessionId(nextSessionId);
    setMessages([]);
    setShowTypingIndicator(false);
    setChatStartedAt(null);
  }

  return (
    <main className="copilot-page">
      <div className="copilot-shell">
        <div className="copilot-layout">
          <aside className="copilot-sidebar" aria-label="Session panel">
            <section className="sidebar-card sidebar-card-primary">
              <p className="sidebar-eyebrow">Session</p>
              <h2 className="sidebar-title">Current Chat</h2>
              <p className="sidebar-text">
                {conversationSummary}. Start a fresh conversation anytime.
              </p>
              <button
                type="button"
                className="sidebar-new-chat-button"
                onClick={handleNewChat}
                disabled={isLoading}
              >
                {isLoading ? "Waiting for Reply..." : "New Chat"}
              </button>
            </section>

            <section className="sidebar-card">
              <h3 className="sidebar-section-title">View Mode</h3>
              <div className="view-mode-toggle" role="group" aria-label="View mode">
                <button
                  type="button"
                  className={`view-mode-button ${
                    viewMode === "user" ? "view-mode-button-active" : ""
                  }`}
                  onClick={() => setViewMode("user")}
                >
                  User View
                </button>
                <button
                  type="button"
                  className={`view-mode-button ${
                    viewMode === "developer" ? "view-mode-button-active" : ""
                  }`}
                  onClick={() => setViewMode("developer")}
                >
                  Developer/Demo
                </button>
              </div>
              <p className="sidebar-text sidebar-text-compact">{viewModeDescription}</p>

              <h3 className="sidebar-section-title">Chat Info</h3>
              <dl className="session-metadata">
                <div className="session-metadata-row">
                  <dt>Status</dt>
                  <dd>
                    <span className={sessionStatusClass}>{sessionStatusLabel}</span>
                  </dd>
                </div>
                <div className="session-metadata-row">
                  <dt>Chat ID</dt>
                  <dd className="session-id">{shortSessionId}</dd>
                </div>
                <div className="session-metadata-row">
                  <dt>Total Messages</dt>
                  <dd>{totalMessageCount}</dd>
                </div>
                <div className="session-metadata-row">
                  <dt>Assistant Replies</dt>
                  <dd>{assistantReplyCount}</dd>
                </div>
                <div className="session-metadata-row">
                  <dt>Started</dt>
                  <dd>{startedAtLabel}</dd>
                </div>
              </dl>
            </section>
          </aside>

          <div className="copilot-main">
            <header className="copilot-header">
              <p className="copilot-eyebrow">AI Customer Support Copilot</p>
              <h1 className="copilot-title">Support Assistant</h1>
              <p className="copilot-subtitle">
                Ask about refunds, shipping, orders, tickets, customers, or support
                policies.
              </p>
            </header>

            <section className="chat-panel">
              <div
                className={`messages-list ${
                  messages.length > 0 ? "messages-list-active" : "messages-list-empty"
                }`}
              >
                <div
                  className={`empty-state ${
                    messages.length === 0 ? "empty-state-visible" : "empty-state-hidden"
                  }`}
                  aria-hidden={messages.length > 0}
                >
                  <h2>Start a conversation</h2>
                  <p className="empty-state-text">
                    Try asking:
                  </p>
                  <ul className="empty-state-list">
                    <li>What is the refund policy?</li>
                    <li>Where is order 1024?</li>
                    <li>What is the status of ticket T-9001?</li>
                    <li>I think this is fraud and I want a manager.</li>
                  </ul>
                </div>

                {messages.map((message, index) => (
                  <MessageBubble
                    key={`${message.role}-${index}`}
                    message={message}
                    viewMode={viewMode}
                  />
                ))}

                {showTypingIndicator && (
                  <div className="message-row message-row-assistant typing-row">
                    <div className="typing-bubble" role="status" aria-live="polite">
                      <span className="typing-label">Support Assistant is typing</span>
                      <span className="typing-dots" aria-hidden="true">
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                      </span>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </section>

            <footer className="chat-input-panel">
              <ChatInput onSend={handleSend} isLoading={isLoading} />
            </footer>
          </div>
        </div>
      </div>
    </main>
  );
}

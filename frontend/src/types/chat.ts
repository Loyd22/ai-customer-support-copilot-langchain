/**
 * Chat-related TypeScript types for the AI Customer Support Copilot frontend.
 *
 * This file defines the API request and response shapes used by the UI.
 */

export type SourceItem = {
  source_id: string;
  title: string;
  snippet: string;
};

export type EscalationInfo = {
  needed: boolean;
  reason: string | null;
};

export type ChatRequest = {
  session_id: string;
  message: string;
};

export type ChatResponse = {
  answer: string;
  action: string;
  used_tools: string[];
  sources: SourceItem[];
  memory_summary: string;
  escalation: EscalationInfo;
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
};
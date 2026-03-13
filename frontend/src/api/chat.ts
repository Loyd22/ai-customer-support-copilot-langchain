/**
 * Chat API client for the AI Customer Support Copilot frontend.
 *
 * This file sends chat requests to the FastAPI backend and returns
 * structured responses for rendering in the UI.
 */

import axios from "axios";
import type { ChatRequest, ChatResponse } from "../types/chat";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

/**
 * Send a chat message to the backend chat endpoint.
 */
export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
  const response = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, payload);
  return response.data;
}
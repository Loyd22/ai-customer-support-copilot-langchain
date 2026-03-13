/**
 * Answer card component for assistant responses.
 *
 * This component renders the assistant answer along with action,
 * tool usage, memory summary, sources, and escalation details.
 */

import type { ChatResponse } from "../types/chat";
import SourceList from "./SourceList";

type AnswerCardProps = {
  response: ChatResponse;
};

export default function AnswerCard({ response }: AnswerCardProps) {
  /**
   * Render tool badges when tools were used in the response.
   */
  function renderTools() {
    if (!response.used_tools.length) {
      return null;
    }

    return (
      <div className="tool-badges">
        {response.used_tools.map((tool) => (
          <span key={tool} className="badge tool-badge">
            {tool}
          </span>
        ))}
      </div>
    );
  }

  return (
    <div className="answer-card">
      <div className="answer-top">
        <span className="badge action-badge">action: {response.action}</span>
        {response.escalation.needed && (
          <span className="badge escalation-badge">needs escalation</span>
        )}
      </div>

      <p className="answer-text">{response.answer}</p>

      {renderTools()}

      <div className="memory-box">
        <strong>Memory summary:</strong>
        <p>{response.memory_summary}</p>
      </div>

      {response.escalation.needed && response.escalation.reason && (
        <div className="escalation-box">
          <strong>Escalation reason:</strong>
          <p>{response.escalation.reason}</p>
        </div>
      )}

      <SourceList sources={response.sources} />
    </div>
  );
}
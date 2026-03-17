/**
 * Answer card component for assistant responses.
 *
 * Purpose:
 * - Make the assistant answer the main visual focus.
 * - Show compact metadata badges below the answer.
 * - Hide secondary technical details behind collapsible sections.
 */

import type { ChatResponse } from "../types/chat";
import type { CopilotViewMode } from "../types/ui";
import type { ReactNode } from "react";
import SourceList from "./SourceList";

type AnswerCardProps = {
  response: ChatResponse;
  viewMode: CopilotViewMode;
};

type DetailsSectionProps = {
  title: string;
  children: ReactNode;
};

/**
 * Convert internal action values into cleaner user-facing labels.
 */
function getActionLabel(action: string): string {
  if (action === "rag") {
    return "Help Center";
  }

  if (action === "tool") {
    return "Internal Systems";
  }

  return "Assistant";
}

/**
 * Standardized collapsible section for secondary response details.
 * Keeps all sections collapsed by default and uses a consistent summary row.
 */
function DetailsSection({ title, children }: DetailsSectionProps) {
  return (
    <details className="answer-details">
      <summary className="answer-details-summary">
        <span className="answer-details-label">{title}</span>
        <span className="answer-details-icon" aria-hidden="true">
          <svg viewBox="0 0 20 20" focusable="false">
            <path d="M5.5 7.75L10 12.25L14.5 7.75" />
          </svg>
        </span>
      </summary>

      <div className="answer-details-content">
        <div className="answer-details-content-inner">{children}</div>
      </div>
    </details>
  );
}

export default function AnswerCard({ response, viewMode }: AnswerCardProps) {
  const actionLabel = getActionLabel(response.action);
  const sourceCount = response.sources.length;
  const toolCount = response.used_tools.length;
  const escalationNeeded = response.escalation.needed;
  const isDeveloperMode = viewMode === "developer";
  const hasTechnicalDetails =
    Boolean(response.action) ||
    toolCount > 0 ||
    Boolean(response.memory_summary) ||
    Boolean(escalationNeeded && response.escalation.reason) ||
    sourceCount > 0;
  const shouldShowMeta = isDeveloperMode || escalationNeeded;
  const escalationLabel = escalationNeeded
    ? isDeveloperMode
      ? "Hand-off Recommended"
      : "May Need Human Support"
    : "No Hand-off Needed";

  /**
   * Render tool badges when tools were used in the response.
   */
  function renderTools() {
    if (!toolCount) {
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
      <div className="answer-main">
        <p className="answer-text">{response.answer}</p>
      </div>

      {isDeveloperMode && (
        <p className="answer-mode-label">Developer/Demo View</p>
      )}

      {shouldShowMeta && (
        <div className="answer-meta">
          {isDeveloperMode && (
            <span className="badge action-badge">{actionLabel}</span>
          )}

          {isDeveloperMode && sourceCount > 0 && (
            <span className="badge meta-badge">
              {sourceCount} Reference{sourceCount > 1 ? "s" : ""}
            </span>
          )}

          {isDeveloperMode && toolCount > 0 && (
            <span className="badge meta-badge">
              {toolCount} System Check{toolCount > 1 ? "s" : ""}
            </span>
          )}

          {(isDeveloperMode || escalationNeeded) && (
            <span
              className={`badge ${escalationNeeded ? "escalation-badge" : "safe-badge"}`}
            >
              {escalationLabel}
            </span>
          )}
        </div>
      )}

      {isDeveloperMode && hasTechnicalDetails && (
        <div className="answer-sections">
          {toolCount > 0 && (
            <DetailsSection title="Tools Used">{renderTools()}</DetailsSection>
          )}

          {response.memory_summary && (
            <DetailsSection title="Conversation Memory">
              <div className="memory-box">
                <p className="answer-section-text">{response.memory_summary}</p>
              </div>
            </DetailsSection>
          )}

          {escalationNeeded && response.escalation.reason && (
            <DetailsSection title="Why Hand-off Is Recommended">
              <div className="escalation-box">
                <p className="answer-section-text">{response.escalation.reason}</p>
              </div>
            </DetailsSection>
          )}

          <DetailsSection title="Routing Action">
            <p className="answer-section-text">{response.action}</p>
          </DetailsSection>

          {sourceCount > 0 && (
            <DetailsSection title={`Raw Sources (${sourceCount})`}>
              <SourceList sources={response.sources} showRawSnippets />
            </DetailsSection>
          )}
        </div>
      )}
    </div>
  );
}

/**
 * Source list component for showing retrieved RAG citations.
 *
 * This component renders source metadata returned by the backend.
 */

import type { SourceItem } from "../types/chat";

type SourceListProps = {
  sources: SourceItem[];
};

export default function SourceList({ sources }: SourceListProps) {
  /**
   * Render nothing when no sources are available.
   */
  if (!sources.length) {
    return null;
  }

  return (
    <div className="source-list">
      <h4>Sources</h4>
      {sources.map((source) => (
        <div key={source.source_id} className="source-card">
          <strong>{source.title}</strong>
          <p>{source.snippet}</p>
        </div>
      ))}
    </div>
  );
}
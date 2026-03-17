/**
 * Source list component for showing retrieved RAG citations.
 *
 * Purpose:
 * - Render a cleaner, lighter source list.
 * - Deduplicate repeated sources.
 * - Shorten long snippets to reduce visual clutter.
 */

import type { SourceItem } from "../types/chat";

type SourceListProps = {
  sources: SourceItem[];
  showRawSnippets?: boolean;
};

/**
 * Shorten long source snippets so the UI stays compact.
 */
function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }

  return `${text.slice(0, maxLength).trim()}...`;
}

/**
 * Deduplicate sources by source ID and title.
 */
function deduplicateSources(sources: SourceItem[]): SourceItem[] {
  const seen = new Set<string>();

  return sources.filter((source) => {
    const key = `${source.source_id}-${source.title}`;

    if (seen.has(key)) {
      return false;
    }

    seen.add(key);
    return true;
  });
}

export default function SourceList({
  sources,
  showRawSnippets = false,
}: SourceListProps) {
  /**
   * Render nothing when no sources are available.
   */
  if (!sources.length) {
    return null;
  }

  const uniqueSources = deduplicateSources(sources);

  return (
    <div className="source-list">
      {uniqueSources.map((source) => (
        <div key={source.source_id} className="source-card">
          <p className="source-title">{source.title}</p>
          <p className="source-snippet">
            {showRawSnippets ? source.snippet : truncateText(source.snippet, 160)}
          </p>
        </div>
      ))}
    </div>
  );
}

# Agent Preferences Reference

## How Preferences Work

Preferences are stored in the `agent-preferences` collection. They map domains to destinations.

A preference record looks like:
```
Routing preference: Operations content goes to practices-and-procedures.
This includes workflows, SOPs, checklists, and development practices.
```

## Query Format

Preferences are stored by DOMAIN, not by specific topic.

| Query Type | Example | Works? |
|------------|---------|--------|
| Domain-based | "What are the user's routing preferences for Operations content?" | Yes |
| Topic-specific | "How has the user routed API authentication notes?" | No |

The domain values come from `get_collection_info()` - fields like "Operations", "Engineering", "Project Management".

## When to Save

| Situation | Action |
|-----------|--------|
| No preference existed | Offer to save |
| User overrode existing preference | Offer to update |
| Preference existed and was followed | Do NOT offer |

## Storage Format

```
ingest_text(
    content="Routing preference: [Domain] content goes to [collection]. This includes [examples of content types].",
    collection_name="agent-preferences",
    document_title="Routing: [Domain]",
    actor_type="[Your AI Assistant Name]"  # See Self-Identification in rag-memory.md
)
```

### Example

```
ingest_text(
    content="Routing preference: Operations content goes to practices-and-procedures. This includes workflows, SOPs, checklists, and development practices.",
    collection_name="agent-preferences",
    document_title="Routing: Operations",
    actor_type="..."  # Your AI assistant product name (validated by backend)
)
```

## Updating Preferences

If user wants to change a preference:
1. Find the existing preference document
2. Use `update_document()` to modify it, OR
3. Use `ingest_text(mode="reingest")` to replace it

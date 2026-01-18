#!/usr/bin/env python3
"""
PreToolUse hook to intercept knowledge base modification operations.
Requires explicit user approval for write operations.

Covers:
- RAG Memory: collections, documents, ingest operations
- Atlassian: Confluence pages/comments, Jira issues/comments/transitions
"""
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow"
        }
    }))
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Map tool names to human-readable operation names
PROTECTED_OPERATIONS = {
    # RAG Memory - Collections
    "mcp__rag-memory__create_collection": "Create Collection",
    "mcp__rag-memory__delete_collection": "Delete Collection",
    "mcp__rag-memory__update_collection_metadata": "Update Collection Metadata",
    # RAG Memory - Documents
    "mcp__rag-memory__update_document": "Update Document",
    "mcp__rag-memory__delete_document": "Delete Document",
    "mcp__rag-memory__manage_collection_link": "Manage Collection Link",
    # RAG Memory - Ingest
    "mcp__rag-memory__ingest_text": "Ingest Text",
    "mcp__rag-memory__ingest_url": "Ingest URL",
    "mcp__rag-memory__ingest_file": "Ingest File",
    "mcp__rag-memory__ingest_directory": "Ingest Directory",
    # Confluence
    "mcp__atlassian__createConfluencePage": "Create Confluence Page",
    "mcp__atlassian__updateConfluencePage": "Update Confluence Page",
    "mcp__atlassian__createConfluenceFooterComment": "Add Confluence Comment",
    "mcp__atlassian__createConfluenceInlineComment": "Add Confluence Inline Comment",
    # Jira
    "mcp__atlassian__createJiraIssue": "Create Jira Issue",
    "mcp__atlassian__editJiraIssue": "Edit Jira Issue",
    "mcp__atlassian__addCommentToJiraIssue": "Add Jira Comment",
    "mcp__atlassian__transitionJiraIssue": "Transition Jira Issue",
    "mcp__atlassian__addWorklogToJiraIssue": "Add Jira Worklog",
}

DESTRUCTIVE_OPERATIONS = {
    "mcp__rag-memory__delete_collection",
    "mcp__rag-memory__delete_document",
}

if tool_name not in PROTECTED_OPERATIONS:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow"
        }
    }))
    sys.exit(0)

operation_name = PROTECTED_OPERATIONS[tool_name]
is_destructive = tool_name in DESTRUCTIVE_OPERATIONS


def format_ingest_operation():
    """Rich formatting for RAG Memory ingest operations."""
    lines = []

    # Header
    lines.append(f"RAG Memory: {operation_name}")
    lines.append("")

    # Common fields
    collection = tool_input.get("collection_name", "Unknown")
    topic = tool_input.get("topic", "(none)")
    mode = tool_input.get("mode", "ingest")

    lines.append(f"Collection: {collection}")
    lines.append(f"Topic: {topic}")

    if mode == "reingest":
        lines.append("⚠️  Mode: REINGEST (will replace existing)")

    lines.append("")

    # Content preview based on ingest type
    if "ingest_text" in tool_name:
        text = tool_input.get("content", "")
        preview = text[:150] + "..." if len(text) > 150 else text
        # Escape newlines for display
        preview = preview.replace("\n", "\\n")
        lines.append(f"Text: \"{preview}\"")

        title = tool_input.get("document_title")
        if title:
            lines.append(f"Title: {title}")
        else:
            lines.append("Title: (auto-generated)")

    elif "ingest_url" in tool_name:
        url = tool_input.get("url", "")
        lines.append(f"URL: {url}")

        follow_links = tool_input.get("follow_links", False)
        max_pages = tool_input.get("max_pages", 10)
        dry_run = tool_input.get("dry_run", False)

        if follow_links:
            lines.append(f"  └─ Crawl up to {max_pages} pages")
        if dry_run:
            lines.append("  └─ DRY RUN (preview only)")

    elif "ingest_file" in tool_name:
        file_path = tool_input.get("file_path", "")
        lines.append(f"File: {file_path}")

    elif "ingest_directory" in tool_name:
        dir_path = tool_input.get("directory_path", "")
        lines.append(f"Directory: {dir_path}")

        extensions = tool_input.get("file_extensions")
        recursive = tool_input.get("recursive", False)

        if extensions:
            lines.append(f"  └─ Types: {', '.join(extensions)}")
        if recursive:
            lines.append("  └─ Recursive: YES")

    # Metadata if present
    metadata = tool_input.get("metadata")
    if metadata:
        lines.append(f"Metadata: {', '.join(metadata.keys())}")

    lines.append("")
    lines.append("Approve?")

    return "\n".join(lines)


def format_generic_operation():
    """Generic formatting for non-ingest operations."""
    lines = []

    if is_destructive:
        lines.append(f"⚠️ DESTRUCTIVE: {operation_name}")
    else:
        lines.append(operation_name)

    lines.append("")
    lines.append("Parameters:")
    for key, value in tool_input.items():
        if isinstance(value, str) and len(value) > 100:
            value = value[:100] + "..."
        lines.append(f"  {key}: {value}")

    if is_destructive:
        lines.append("")
        lines.append("⚠️ This action cannot be undone")

    lines.append("")
    lines.append("Approve?")

    return "\n".join(lines)


# Choose formatting based on operation type
if tool_name.startswith("mcp__rag-memory__ingest_"):
    message = format_ingest_operation()
else:
    message = format_generic_operation()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message
    }
}))
sys.exit(0)

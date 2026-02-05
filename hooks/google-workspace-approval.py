#!/usr/bin/env python3
"""
PreToolUse hook to intercept Google Workspace modification operations.
Requires explicit user approval for write operations.

Covers:
- Docs: create, modify text
- Drive: create file, update file, share file
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

PROTECTED_OPERATIONS = {
    # Docs
    "mcp__google-workspace__create_doc": "Create Google Doc",
    "mcp__google-workspace__modify_doc_text": "Modify Google Doc",
    # Drive
    "mcp__google-workspace__create_drive_file": "Create Drive File",
    "mcp__google-workspace__update_drive_file": "Update Drive File",
    "mcp__google-workspace__share_drive_file": "Share Drive File",
}

DESTRUCTIVE_OPERATIONS = set()

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


def format_operation():
    """Rich formatting for Google Workspace operations."""
    lines = []

    lines.append(f"Google Workspace: {operation_name}")
    lines.append("")

    if "create_doc" in tool_name:
        title = tool_input.get("title", "")
        lines.append(f"Title: {title}")

    elif "modify_doc" in tool_name:
        doc_id = tool_input.get("documentId", "")
        lines.append(f"Document: {doc_id[:20]}..." if len(doc_id) > 20 else f"Document: {doc_id}")
        operations = tool_input.get("operations", [])
        if operations:
            lines.append(f"Operations: {len(operations)} changes")

    elif "create_drive_file" in tool_name:
        name = tool_input.get("name", "")
        mime_type = tool_input.get("mimeType", "")
        parents = tool_input.get("parents", [])
        lines.append(f"Name: {name}")
        if mime_type:
            lines.append(f"Type: {mime_type}")
        if parents:
            lines.append(f"Folder: {parents[0][:20]}..." if len(parents[0]) > 20 else f"Folder: {parents[0]}")

    elif "update_drive_file" in tool_name:
        file_id = tool_input.get("fileId", "")
        lines.append(f"File: {file_id[:20]}..." if len(file_id) > 20 else f"File: {file_id}")

    elif "share_drive_file" in tool_name:
        file_id = tool_input.get("fileId", "")
        email = tool_input.get("email", "")
        role = tool_input.get("role", "")
        lines.append(f"File: {file_id[:20]}..." if len(file_id) > 20 else f"File: {file_id}")
        lines.append(f"Share with: {email}")
        lines.append(f"Role: {role}")

    lines.append("")
    lines.append("Approve?")

    return "\n".join(lines)


message = format_operation()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message
    }
}))
sys.exit(0)

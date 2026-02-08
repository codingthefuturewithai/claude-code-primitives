#!/usr/bin/env python3
"""
PreToolUse hook to intercept Google Drive modification operations.
Requires explicit user approval for write operations.

Covers:
- Upload file to Google Drive
- Create folder in Google Drive
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
    "mcp__google-drive__upload_file": "Upload File to Google Drive",
    "mcp__google-drive__create_folder": "Create Google Drive Folder",
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
    """Rich formatting for Google Drive operations."""
    lines = []

    lines.append(f"Google Drive: {operation_name}")
    lines.append("")

    if "upload_file" in tool_name:
        local_path = tool_input.get("local_path", "")
        folder_id = tool_input.get("folder_id", "")
        file_name = tool_input.get("file_name", "")
        lines.append(f"File: {local_path}")
        if file_name:
            lines.append(f"Name: {file_name}")
        if folder_id:
            lines.append(f"Folder: {folder_id[:20]}..." if len(folder_id) > 20 else f"Folder: {folder_id}")

    elif "create_folder" in tool_name:
        folder_name = tool_input.get("folder_name", "")
        parent = tool_input.get("parent_folder_id", "")
        lines.append(f"Folder: {folder_name}")
        if parent:
            lines.append(f"Parent: {parent[:20]}..." if len(parent) > 20 else f"Parent: {parent}")

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

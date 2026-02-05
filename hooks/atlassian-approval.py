#!/usr/bin/env python3
"""
PreToolUse hook to intercept Atlassian modification operations.
Requires explicit user approval for write operations.

Covers:
- Confluence: pages, footer comments, inline comments
- Jira: issues, comments, transitions, worklogs
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
    """Format Atlassian operations for approval display."""
    lines = []

    if is_destructive:
        lines.append(f"⚠️ DESTRUCTIVE: {operation_name}")
    else:
        lines.append(f"Atlassian: {operation_name}")

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


message = format_operation()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message
    }
}))
sys.exit(0)

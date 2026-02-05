#!/usr/bin/env python3
"""
PreToolUse hook to intercept GitLab modification operations.
Requires explicit user approval for write operations.

Covers:
- Issues: create, update, delete
- Merge Requests: create, update
- Notes: create (comments on issues/MRs)
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
    "mcp__gitlab__create_issue": "Create GitLab Issue",
    "mcp__gitlab__update_issue": "Update GitLab Issue",
    "mcp__gitlab__delete_issue": "Delete GitLab Issue",
    "mcp__gitlab__create_merge_request": "Create GitLab Merge Request",
    "mcp__gitlab__update_merge_request": "Update GitLab Merge Request",
    "mcp__gitlab__create_note": "Add GitLab Comment",
}

DESTRUCTIVE_OPERATIONS = {
    "mcp__gitlab__delete_issue",
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


def format_operation():
    """Rich formatting for GitLab operations."""
    lines = []

    if is_destructive:
        lines.append(f"⚠️ DESTRUCTIVE: {operation_name}")
    else:
        lines.append(f"GitLab: {operation_name}")

    lines.append("")

    project_id = tool_input.get("project_id", "")
    if project_id:
        lines.append(f"Project: {project_id}")

    if "issue" in tool_name:
        issue_iid = tool_input.get("issue_iid", tool_input.get("iid", ""))
        title = tool_input.get("title", "")
        if issue_iid:
            lines.append(f"Issue: #{issue_iid}")
        if title:
            lines.append(f"Title: {title}")

    if "merge_request" in tool_name:
        mr_iid = tool_input.get("merge_request_iid", tool_input.get("iid", ""))
        title = tool_input.get("title", "")
        source = tool_input.get("source_branch", "")
        target = tool_input.get("target_branch", "")
        if mr_iid:
            lines.append(f"MR: !{mr_iid}")
        if title:
            lines.append(f"Title: {title}")
        if source and target:
            lines.append(f"Branches: {source} → {target}")

    if "note" in tool_name:
        body = tool_input.get("body", "")
        preview = body[:100] + "..." if len(body) > 100 else body
        lines.append(f"Comment: \"{preview}\"")

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

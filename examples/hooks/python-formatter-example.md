# Hook Example: Python Auto-Formatter

This is a working example of a PostToolUse hook that automatically formats Python files after they are written or edited.

## Configuration Location

Hooks are configured in `settings.json`:
- **Global**: `~/.claude/settings.json`
- **Project**: `.claude/settings.json`

## Complete Implementation

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_USE_ARGS\" == *\".py\"* ]]; then black \"$(echo \"$CLAUDE_TOOL_USE_ARGS\" | grep -oE '[^\"]+\\.py' | head -1)\"; fi",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## How It Works

**Trigger**: After any `Write` or `Edit` tool completes

**Matcher**: `"Write|Edit"` - Regex pattern matching tool names

**Action**:
1. Check if the file path contains `.py`
2. If yes, extract the Python file path
3. Run `black` formatter on that file
4. Timeout after 30 seconds

**Result**: All Python files are automatically formatted when created or edited

## Key Features

### 1. Event Type

```json
"PostToolUse": [...]
```

Runs AFTER Write/Edit completes, so the file exists when black runs.

### 2. Tool Matcher

```json
"matcher": "Write|Edit"
```

- **Pattern**: Regex matching tool names
- **Write|Edit**: Matches either Write OR Edit tool
- **Case-sensitive**: Must match exact tool names

Alternative matchers:
- `"*"` - Match all tools
- `"Write"` - Only Write tool
- `"Edit|Notebook.*"` - Edit or any Notebook tool

### 3. Hook Type

```json
"type": "command"
```

Executes a bash command. Alternative is `"prompt"` (for Stop/SubagentStop events).

### 4. Timeout

```json
"timeout": 30
```

Kill the hook if it takes longer than 30 seconds. Prevents hanging on large files.

## Environment Variables Available

The hook has access to:

- `$CLAUDE_PROJECT_DIR` - Project root directory
- `$CLAUDE_TOOL_USE_ARGS` - JSON string of tool arguments
- `$CLAUDE_TOOL_USE_RESULT` - Tool execution result

## Matcher Patterns

### Simple Tool Match
```json
"matcher": "Write"
```
Matches only the Write tool.

### Multiple Tools (Regex OR)
```json
"matcher": "Write|Edit|NotebookEdit"
```
Matches any of these tools.

### Wildcard (All Tools)
```json
"matcher": "*"
```
Matches every tool execution.

### MCP Tools
```json
"matcher": "mcp__.*__.*"
```
Matches all MCP server tools.

## Exit Code Behavior

The hook command's exit code controls flow:

- **0**: Success, continue normally
- **1-255**: Error logged, but execution continues
- Hook cannot block tool execution (it runs AFTER)

For blocking behavior, use `PreToolUse` or `PermissionRequest` events.

## Best Practices Demonstrated

### ✅ Defensive Scripting

```bash
if [[ \"$CLAUDE_TOOL_USE_ARGS\" == *\".py\"* ]]; then
  # Only run if file is Python
fi
```

Checks file extension before running formatter. Prevents errors on non-Python files.

### ✅ Timeout Protection

```json
"timeout": 30
```

Prevents hook from hanging indefinitely on large files or slow systems.

### ✅ Focused Matcher

```json
"matcher": "Write|Edit"
```

Only runs on file modification tools, not Read, Grep, etc. Avoids unnecessary executions.

## Common Mistakes to Avoid

### ❌ Missing Timeout

```json
{
  "type": "command",
  "command": "black $FILE"
  // Missing timeout - could hang forever
}
```

### ✅ Include Timeout

```json
{
  "type": "command",
  "command": "black $FILE",
  "timeout": 30
}
```

### ❌ Wrong Event Type

```json
"PreToolUse": [  // WRONG - file doesn't exist yet!
  {
    "matcher": "Write",
    "hooks": [
      {
        "type": "command",
        "command": "black $FILE"
      }
    ]
  }
]
```

### ✅ Correct Event Type

```json
"PostToolUse": [  // CORRECT - file exists after Write
  {
    "matcher": "Write",
    "hooks": [
      {
        "type": "command",
        "command": "black $FILE"
      }
    ]
  }
]
```

### ❌ Overly Broad Matcher

```json
"matcher": "*"  // Runs on EVERY tool - wasteful
```

### ✅ Specific Matcher

```json
"matcher": "Write|Edit"  // Only file modifications
```

## Testing the Hook

1. Add to `~/.claude/settings.json` for global scope
2. Or add to `.claude/settings.json` for project scope
3. Ensure `black` is installed:
   ```bash
   pip install black
   ```
4. Test by creating a Python file:
   ```
   # In Claude Code:
   Create a new Python file with some unformatted code
   ```
5. Verify:
   - File is automatically formatted after Write completes
   - Check Claude Code logs for hook execution

## Alternative Implementations

### Using External Script

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/scripts/format-python.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**scripts/format-python.sh:**
```bash
#!/bin/bash
set -e

# Extract file path from tool args
FILE=$(echo "$CLAUDE_TOOL_USE_ARGS" | jq -r '.file_path // .path // empty')

# Only format Python files
if [[ "$FILE" == *.py ]]; then
    echo "Formatting $FILE with black..."
    black "$FILE"
    echo "✓ Formatted successfully"
fi
```

### Multiple Formatters

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/scripts/auto-format.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**auto-format.sh:**
```bash
#!/bin/bash
FILE=$(echo "$CLAUDE_TOOL_USE_ARGS" | jq -r '.file_path // .path // empty')

case "$FILE" in
    *.py)
        black "$FILE"
        ;;
    *.js|*.ts|*.jsx|*.tsx)
        prettier --write "$FILE"
        ;;
    *.go)
        gofmt -w "$FILE"
        ;;
esac
```

## Scope Considerations

**Global scope** (`~/.claude/settings.json`):
- Applies to ALL projects
- Good for personal preferences (formatting, linting)

**Project scope** (`.claude/settings.json`):
- Applies only to current project
- Good for team standards
- Can be committed to git

## Performance Impact

Hooks add latency to tool execution:
- **PostToolUse**: Runs after tool completes
- **Timeout**: 30 seconds max
- **Black execution**: ~100-500ms for typical files

For large codebases, consider:
1. Increase timeout for large files
2. Use async execution if available
3. Only run on specific file patterns

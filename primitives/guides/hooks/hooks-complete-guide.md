# Hooks: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: hook
- content_type: complete-guide
- version: 1.0

---

## What Are Claude Code Hooks?

Claude Code hooks are **JSON configuration entries** in `settings.json` or `config.json` that trigger shell commands at specific lifecycle events during Claude Code operations.

**CRITICAL: Hooks are NOT files you create.** They are JSON configuration you add to existing settings files.

### Hooks vs Git Hooks

| Claude Code Hooks | Git Hooks |
|------------------|-----------|
| JSON config in settings.json | Shell scripts in .git/hooks/ |
| Trigger on tool lifecycle events | Trigger on git operations |
| Configured via Claude Code settings | Created as executable files |
| Run shell commands you specify | ARE the shell script |

**NEVER create shell script files when asked to create a Claude Code hook.** You're configuring behavior, not writing scripts.

---

## When to Use Hooks

Use hooks when:
- **Automatic enforcement required** - Action MUST happen every time (e.g., format code after every edit)
- **No user decision needed** - Action is non-negotiable policy
- **Event-driven automation** - React to tool lifecycle events
- **Cross-project enforcement** - Same behavior across all projects (use global `~/.claude/config.json`)

Do NOT use hooks when:
- User should decide when to run (use Slash Command instead)
- Complex multi-step logic needed (use Skill instead)
- Need to process output or make decisions (use Skill instead)

---

## Available Lifecycle Events

Hooks can trigger on these events:

### 1. PostToolUse
**When:** After any tool executes successfully
**Use for:**
- Auto-formatting code after Edit/Write
- Logging tool usage
- Cleanup operations
- Validation after changes

**Example:**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}",
      "Write": "black {file_path}"
    }
  }
}
```

### 2. PreToolUse
**When:** Before any tool executes
**Use for:**
- Pre-flight validation
- Backup operations
- Permission checks
- Setup tasks

**Example:**
```json
{
  "hooks": {
    "PreToolUse": {
      "Write": "mkdir -p $(dirname {file_path})"
    }
  }
}
```

### 3. UserPromptSubmit
**When:** When user submits a prompt
**Use for:**
- Session logging
- Analytics
- Context preparation

**Example:**
```json
{
  "hooks": {
    "UserPromptSubmit": "echo '{timestamp}: {prompt}' >> ~/.claude/logs/prompts.log"
  }
}
```

### 4. ModelResponse
**When:** After model generates response
**Use for:**
- Response logging
- Analytics
- Post-processing

**Example:**
```json
{
  "hooks": {
    "ModelResponse": "echo 'Response generated' >> ~/.claude/logs/activity.log"
  }
}
```

---

## Configuration Format

### Global Hooks (`~/.claude/config.json`)

Apply to ALL projects:

```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}",
      "Write": "black {file_path}"
    },
    "PreToolUse": {
      "Bash": "echo 'Running: {command}' >> ~/.claude/logs/bash.log"
    }
  }
}
```

### Project Hooks (`.claude/settings.json`)

Apply to specific project only:

```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "npm run lint:fix {file_path}",
      "Write": "npm run lint:fix {file_path}"
    }
  }
}
```

### Available Variables

Hooks can use these template variables:

- `{file_path}` - Path to file being operated on (Edit, Write, Read tools)
- `{command}` - Command being executed (Bash tool)
- `{prompt}` - User's prompt text (UserPromptSubmit event)
- `{timestamp}` - Current timestamp
- `{tool_name}` - Name of tool being invoked

---

## Working Examples

### Example 1: Auto-format Python on Every Edit

**Requirement:** "Automatically format Python code with Black after every file edit"

**Configuration (`~/.claude/config.json`):**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}",
      "Write": "black {file_path}"
    }
  }
}
```

**Why this works:**
- PostToolUse triggers AFTER Edit/Write succeed
- {file_path} is replaced with actual file path
- Black runs on the file that was just modified
- Happens automatically, no user action needed

### Example 2: Log All Bash Commands

**Requirement:** "Keep audit log of all bash commands Claude runs"

**Configuration (`~/.claude/config.json`):**
```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "echo '[{timestamp}] {command}' >> ~/.claude/logs/bash-audit.log"
    }
  }
}
```

**Why this works:**
- PreToolUse triggers BEFORE Bash executes
- Creates audit trail before command runs
- {timestamp} and {command} are replaced with actual values
- Log file persists across sessions

### Example 3: Project-Specific Linting

**Requirement:** "Run ESLint fix after editing JavaScript files in this project only"

**Configuration (`.claude/settings.json` in project root):**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "npx eslint --fix {file_path}",
      "Write": "npx eslint --fix {file_path}"
    }
  }
}
```

**Why this works:**
- Project-level settings only apply to this project
- Uses npx to run ESLint from project dependencies
- Fixes linting issues automatically after edits

### Example 4: Multi-Tool Hook

**Requirement:** "Format code differently based on file type"

**Configuration (`~/.claude/config.json`):**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "~/.claude/scripts/format-by-extension.sh {file_path}",
      "Write": "~/.claude/scripts/format-by-extension.sh {file_path}"
    }
  }
}
```

**Script (`~/.claude/scripts/format-by-extension.sh`):**
```bash
#!/bin/bash
FILE="$1"
EXT="${FILE##*.}"

case "$EXT" in
  py)
    black "$FILE"
    ;;
  js|jsx|ts|tsx)
    npx prettier --write "$FILE"
    ;;
  go)
    gofmt -w "$FILE"
    ;;
esac
```

**Why this works:**
- Hook calls external script for complex logic
- Script handles multiple formatters based on extension
- Single hook configuration, extensible logic

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Creating Shell Script Files

**WRONG:**
```markdown
Creating file: ~/.claude/hooks/python-format.sh

#!/bin/bash
black "$1"
```

**Why it's wrong:** Claude Code hooks are JSON config, not shell script files. The `.claude/hooks/` directory should NOT exist.

**RIGHT:**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}"
    }
  }
}
```

### ❌ Anti-Pattern 2: Using Hooks for Complex Logic

**WRONG:**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "if grep -q 'TODO' {file_path}; then echo 'TODOs found'; git commit -m 'WIP'; fi"
    }
  }
}
```

**Why it's wrong:** Hooks should be simple, deterministic commands. Complex logic should be in Skills or external scripts.

**RIGHT:** Create a Skill that activates on Edit and contains the TODO analysis logic.

### ❌ Anti-Pattern 3: Hooks for User-Invoked Actions

**WRONG:** Creating hook to run tests when user wants to test

**Why it's wrong:** User should control when tests run. Use Slash Command instead.

**RIGHT:**
```markdown
---
description: Run project tests
---

Run the test suite for this project using pytest.
```

### ❌ Anti-Pattern 4: Installing Git Hooks

**WRONG:**
```bash
# Creating .git/hooks/pre-commit
cp python-format.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Why it's wrong:** Git hooks and Claude Code hooks are completely different systems.

**RIGHT:** Configure Claude Code hooks in settings.json to trigger on Claude's tool lifecycle events.

---

## Content Crafting: Instructions vs Documentation

When configuring hooks, write the JSON as **configuration**, not explanation:

**❌ Documentation style:**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "This hook will run Black formatter on Python files after editing"
    }
  }
}
```

**✅ Instructions style:**
```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "black {file_path}"
    }
  }
}
```

The hook value is the COMMAND to execute, not a description.

---

## How to Help Developers Create Hooks

When a developer asks to create a hook:

### Step 1: Confirm Hook is Right Choice

Ask:
- "Should this happen automatically every time, or only when you decide?"
- If "only when I decide" → Recommend Slash Command instead
- If "automatically every time" → Proceed with hook

### Step 2: Identify Lifecycle Event

Based on their need:
- "After editing files" → PostToolUse on Edit/Write
- "Before running commands" → PreToolUse on Bash
- "Log my prompts" → UserPromptSubmit
- "Track responses" → ModelResponse

### Step 3: Gather Command Details

Ask:
- "What command should run?"
- "Does this need to work across all projects or just this one?"
- "Are there any variables needed (file path, timestamp, etc)?"

### Step 4: Determine Configuration Location

- All projects → `~/.claude/config.json`
- This project only → `.claude/settings.json`

### Step 5: Provide Configuration JSON

Give them the exact JSON to add:

```json
{
  "hooks": {
    "[EventType]": {
      "[ToolName]": "[command with {variables}]"
    }
  }
}
```

### Step 6: Explain Manual Configuration

Tell them:
1. Open the appropriate config file
2. Add or merge the hooks section
3. Save the file
4. Restart Claude Code if needed

**NEVER create files.** Only provide configuration JSON.

---

## Testing Hooks

How to verify hooks work:

### Test PostToolUse Hook

1. Configure hook:
```json
{
  "hooks": {
    "PostToolUse": {
      "Write": "echo 'File written: {file_path}' >> /tmp/hook-test.log"
    }
  }
}
```

2. Use Write tool to create a file
3. Check `/tmp/hook-test.log` for entry
4. Verify {file_path} was replaced with actual path

### Test PreToolUse Hook

1. Configure hook:
```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "echo 'About to run: {command}' >> /tmp/hook-test.log"
    }
  }
}
```

2. Use Bash tool to run a command
3. Check log appears BEFORE command executes
4. Verify {command} was replaced with actual command

---

## Common Mistakes When Creating Hooks

### Mistake 1: Treating Hooks as Primitives You Create

**What developers think:** "Create a hook file in .claude/hooks/"

**Reality:** Hooks are JSON config in settings.json, not files you create

**Fix:** YOU read settings.json, add the hook JSON, and write it back. Never tell developer to manually edit.

### Mistake 2: Confusing with Git Hooks

**What developers think:** "Create a pre-commit hook in .git/hooks/"

**Reality:** Claude Code hooks are separate from Git hooks

**Fix:** Explain the difference (see table at top of guide)

### Mistake 3: Complex Logic in Hook Commands

**What developers think:** Hook command can have if/else logic

**Reality:** Hooks should call simple commands or external scripts

**Fix:** Move complex logic to external script, hook calls script

### Mistake 4: Using Hooks for User-Controlled Actions

**What developers think:** "Create hook to run tests"

**Reality:** Tests should be user-invoked (Slash Command)

**Fix:** Recommend Slash Command instead of hook

---

## Summary Checklist

When helping create a hook, verify:

- [ ] Hook is right choice (automatic enforcement needed?)
- [ ] Identified correct lifecycle event (PostToolUse, PreToolUse, etc)
- [ ] Identified correct tool (Edit, Write, Bash, etc)
- [ ] Command is simple and deterministic
- [ ] Used correct variables ({file_path}, {command}, etc)
- [ ] Chose right config file (global vs project)
- [ ] Read config file, added hook JSON, wrote it back automatically
- [ ] Confirmed with developer what was created
- [ ] Did NOT create any shell script files
- [ ] Did NOT confuse with Git hooks

---

## Reference

**Official Claude Code Hooks Documentation:**
- [Settings Reference](https://docs.anthropic.com/claude/docs/claude-code-settings)
- [Hooks Configuration](https://docs.anthropic.com/claude/docs/hooks)

**Valid Event Types:** PostToolUse, PreToolUse, UserPromptSubmit, ModelResponse

**Valid Tool Names:** Edit, Write, Read, Bash, Task, Glob, Grep, LSP, etc.

**Configuration Files:**
- Global: `~/.claude/config.json`
- Project: `.claude/settings.json`

**Template Variables:** {file_path}, {command}, {prompt}, {timestamp}, {tool_name}

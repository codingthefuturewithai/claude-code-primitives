# Subagent Example: code-reviewer

This is a working example of a subagent for comprehensive code review with isolated context and skill access.

## File Location

```
agents/code-reviewer.md
```

## Complete Implementation

See `code-reviewer.md` for the full implementation.

## Key Features

### 1. Required Frontmatter Fields

```yaml
name: code-reviewer
description: Reviews code for quality, best practices, and potential issues...
```

- **name** (required): Unique identifier, lowercase with hyphens
- **description** (required): When this subagent should be invoked

### 2. Optional Configuration

```yaml
tools: Read, Grep, Glob, Write
model: opus
skills: security-reviewer
```

- **tools**: Specific tools available (if omitted, inherits all tools)
- **model**: `opus`, `sonnet`, `haiku`, or `inherit`
- **skills**: Explicit skill access (subagents don't inherit parent skills!)

### 3. Tool Restrictions

```yaml
tools: Read, Grep, Glob, Write
```

This subagent can:
- ✅ Read files
- ✅ Search code (Grep, Glob)
- ✅ Write review reports
- ❌ Execute bash commands (not in tools list)
- ❌ Edit files directly (review only)

### 4. Explicit Skill Access

```yaml
skills: security-reviewer
```

**Critical**: Subagents don't inherit skills from parent conversation. Must explicitly list them.

Without this field, the security-reviewer skill would NOT be available even if it's loaded in the main conversation.

### 5. Model Selection

```yaml
model: opus
```

Uses Claude Opus for deeper, more thorough code analysis. Alternative options:
- `sonnet` - Balanced performance
- `haiku` - Faster, simpler tasks
- `inherit` - Use main conversation's model

## How It Works

**Invocation from slash command**:
```markdown
---
description: Review code changes
allowed-tools: Task
---

Use Task tool to invoke the code-reviewer subagent.
```

**Direct invocation**:
```
Use the code-reviewer subagent to analyze src/auth/
```

**Execution**:
1. Subagent starts with isolated context
2. Has access only to specified tools
3. security-reviewer skill auto-activates when needed
4. Generates comprehensive review report
5. Returns results to main conversation

## Best Practices Demonstrated

### ✅ Clear Responsibility Definition

```markdown
## Responsibilities

Perform thorough code review covering:
1. **Code Quality**
2. **Best Practices**
3. **Security**
4. **Performance**
```

### ✅ Systematic Workflow

```markdown
## Review Process

### Phase 1: Understand Context
### Phase 2: Quality Analysis
### Phase 3: Security Analysis
### Phase 4: Performance Review
### Phase 5: Generate Report
```

### ✅ Structured Output

Specifies exact format for review reports, ensuring consistency.

### ✅ Tool Justification

```markdown
## Tool Usage

- **Read**: Examine source files
- **Grep**: Search for patterns
- **Glob**: Find related files
- **Write**: Create review report
```

Explains why each tool is needed.

## When to Use Subagents

Use subagents when you need:

1. **Isolated Context**
   - Subagent doesn't see main conversation history
   - Fresh perspective on the task

2. **Parallel Execution**
   - Run multiple subagents simultaneously
   - Only option for parallel work in Claude Code

3. **Tool Restrictions**
   - Limit which tools are available
   - Prevent unintended actions

4. **Specific Skills**
   - Load particular skills for specialized work
   - Skills don't auto-load from parent

5. **Model Selection**
   - Use different model than main conversation
   - Opus for complex analysis, haiku for simple tasks

## Composition Pattern

This example demonstrates:

**Slash Command → Subagent → Skill**

```
/review-pr  (Slash Command)
  ↓ uses Task tool
code-reviewer (Subagent)
  ↓ has access to
security-reviewer (Skill - auto-activates)
```

This is a valid composition pattern.

## Common Mistakes to Avoid

### ❌ Assuming Skill Inheritance

```yaml
# WRONG - assumes security-reviewer is available
# (It's not, unless explicitly listed!)
name: code-reviewer
description: Reviews code
tools: Read, Write
```

### ✅ Explicit Skill Declaration

```yaml
# CORRECT
name: code-reviewer
description: Reviews code
tools: Read, Write
skills: security-reviewer
```

### ❌ Wrong Filename Pattern

```
# WRONG
agents/code-reviewer/AGENT.md
agents/CODE-REVIEWER.md

# CORRECT
agents/code-reviewer.md
```

### ❌ Omitting Tools Field When Restrictions Needed

```yaml
# WRONG - inherits ALL tools including Bash
name: code-reviewer
description: Reviews code
```

If you need tool restrictions, specify the `tools` field.

## Testing the Subagent

1. Install the subagent:
   ```bash
   cp code-reviewer.md ~/.claude/agents/
   ```

2. Install required skill:
   ```bash
   cp -r ../skills/security-reviewer ~/.claude/skills/
   ```

3. Test invocation:
   ```
   # In Claude Code:
   Use the code-reviewer subagent to review src/auth/login.py
   ```

4. Verify:
   - Subagent activates
   - security-reviewer skill auto-loads
   - Review report is generated
   - Only allowed tools are used

## Extension Points

To enhance this subagent:

1. **Add more skills**:
   ```yaml
   skills: security-reviewer, performance-analyzer
   ```

2. **Adjust tool access**:
   ```yaml
   tools: Read, Grep, Glob, Write, Task
   ```
   Adding `Task` allows the subagent to spawn additional subagents.

3. **Change model based on task**:
   ```yaml
   model: haiku  # For quick syntax checks
   model: opus   # For deep architectural review
   ```

## Performance Considerations

**Why opus?**
Code review benefits from:
- Deeper reasoning about code patterns
- Better understanding of architectural implications
- More thorough security analysis

For simpler tasks (syntax check, formatting review), use `haiku` or `sonnet`.

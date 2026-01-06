# Skill Example: security-reviewer

This is a working example of a skill that auto-activates for security code review tasks.

## File Structure

```
skills/
└── security-reviewer/
    └── SKILL.md
```

**Critical**: The filename MUST be `SKILL.md` (uppercase).

## Complete Implementation

See `security-reviewer/SKILL.md` for the full implementation.

## Key Features

### 1. Third-Person Description (CRITICAL)

```yaml
description: Reviews code for security vulnerabilities...
```

✅ **Correct**: "Reviews code" (third person)
❌ **Wrong**: "I can review code" or "You can use this to review code"

**Why**: The description is injected into the system prompt. Inconsistent point-of-view causes discovery problems.

### 2. Gerund Form Name

```yaml
name: security-reviewer
```

✅ **Correct**: `security-reviewer` (describes what it does)
❌ **Wrong**: `security-helper` (generic "helper" suffix)

### 3. Clear Activation Triggers

```yaml
description: ...Use when analyzing code security, reviewing pull requests, or when user mentions security, vulnerabilities, or OWASP.
```

Includes keywords that trigger activation:
- "security"
- "vulnerabilities"
- "OWASP"
- "reviewing pull requests"

### 4. Tool Restrictions

```yaml
allowed-tools: Read, Grep, Glob
```

Only allows necessary tools:
- `Read` - Read source files
- `Grep` - Search for patterns
- `Glob` - Find files

Does NOT allow `Write`, `Edit`, or `Bash` - this is a review-only skill.

### 5. Structured Workflow

The skill provides a clear process:
1. Scan for critical patterns
2. Review authentication flow
3. Check dependencies
4. Report findings

This ensures consistent, thorough analysis.

### 6. Output Format Specified

```markdown
## Output Format

Structure findings as:
...
```

Provides a template for how to present results. This ensures consistent, actionable output.

## How It Works

**Activation**: When user says something like:
- "Review this code for security issues"
- "Check for vulnerabilities"
- "OWASP compliance check"

**Execution**:
1. Claude automatically loads this skill
2. Uses Grep to search for vulnerable patterns
3. Uses Read to examine authentication code
4. Provides structured security report

**No manual invocation needed** - the skill auto-activates based on context.

## Best Practices Demonstrated

### ✅ Write as Instructions (What to DO)

```markdown
Analyze code for security vulnerabilities following OWASP Top 10 guidelines.

When activated, perform systematic security analysis:
1. **Injection Flaws**
   - SQL injection
   - Command injection
```

### ❌ NOT as Documentation (What it IS)

```markdown
This skill helps Claude understand security vulnerabilities...

The purpose of this skill is to provide security analysis...
```

### ✅ Progressive Disclosure

The SKILL.md is under 100 lines. For a more complex security skill, you would:
1. Keep SKILL.md concise (overview + workflow)
2. Move detailed patterns to `patterns.md`
3. Move example fixes to `examples.md`
4. Link to them: "See patterns.md for comprehensive vulnerability patterns"

### ✅ Specific, Not Generic

Description mentions specific capabilities:
- "injection flaws"
- "authentication issues"
- "sensitive data exposure"
- "OWASP Top 10"

Not: "Helps with security" or "Analyzes code quality"

## Common Mistakes to Avoid

### ❌ Wrong Point of View

```yaml
# WRONG
description: I can help you review code for security issues

# CORRECT
description: Reviews code for security vulnerabilities...
```

### ❌ Generic Name

```yaml
# WRONG
name: security-helper

# CORRECT
name: security-reviewer
```

### ❌ Vague Description

```yaml
# WRONG
description: Security analysis tool

# CORRECT
description: Reviews code for security vulnerabilities including injection flaws, authentication issues, and sensitive data exposure. Use when analyzing code security, reviewing pull requests, or when user mentions security, vulnerabilities, or OWASP.
```

### ❌ Wrong Filename

```
# WRONG
skills/security-reviewer/skill.md
skills/security-reviewer/security-reviewer.md

# CORRECT
skills/security-reviewer/SKILL.md
```

## Testing the Skill

1. Install the skill:
   ```bash
   cp -r security-reviewer/ ~/.claude/skills/
   ```

2. Test activation:
   ```
   # In Claude Code, say:
   "Review this auth.py file for security issues"
   ```

3. Verify:
   - Skill auto-activates
   - Uses only allowed tools (Read, Grep, Glob)
   - Provides structured security report

## Extension Points

To enhance this skill:

1. **Add supporting patterns file**:
   ```
   security-reviewer/
   ├── SKILL.md
   └── vulnerability-patterns.md
   ```

2. **Add examples**:
   ```
   security-reviewer/
   ├── SKILL.md
   ├── vulnerability-patterns.md
   └── fix-examples.md
   ```

3. **Add scripts**:
   ```
   security-reviewer/
   ├── SKILL.md
   └── scripts/
       └── scan.py
   ```

Reference from SKILL.md: "See vulnerability-patterns.md for comprehensive pattern list"

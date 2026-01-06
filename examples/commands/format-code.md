# Slash Command Example: format-code

This is a working example of a slash command that formats code files using appropriate formatters.

## File Location

```
commands/format-code.md
```

## Complete Implementation

```markdown
---
description: Format code files using appropriate formatter (black, prettier, etc.)
argument-hint: [file-path]
allowed-tools: Read, Bash, Write
model: haiku
---

# Format Code

Format the code file at $1 using the appropriate formatter based on file extension.

## Steps

1. Use Read tool to verify file exists
2. Determine file type from extension:
   - `.py` → black
   - `.js`, `.ts`, `.jsx`, `.tsx` → prettier
   - `.go` → gofmt
   - `.rs` → rustfmt
3. Use Bash tool to run formatter
4. Report results

## Error Handling

If no formatter is available for the file type, report which file types are supported.

If formatter is not installed, provide installation instructions.
```

## How It Works

**Invocation:**
```
/format-code src/main.py
```

**What happens:**
1. Claude reads `src/main.py` to verify it exists
2. Detects `.py` extension → uses `black`
3. Runs `black src/main.py`
4. Reports success or provides errors

## Key Features

- **argument-hint**: Shows user what arguments to provide
- **allowed-tools**: Restricts to only necessary tools (Read, Bash, Write)
- **model: haiku**: Uses faster model for simple formatting task
- **$1**: References first argument (the file path)

## Best Practices Demonstrated

1. **Clear description**: User knows exactly what this does
2. **Argument placeholder**: $1 makes it clear where the file path goes
3. **Tool restriction**: Only allows Read, Bash, Write - prevents unnecessary tool use
4. **Appropriate model**: haiku is sufficient for this simple task
5. **Error handling**: Instructions include what to do when things go wrong

## Common Mistakes to Avoid

❌ **Don't write as documentation:**
```markdown
This command helps Claude format code files by detecting the file type...
```

✅ **Write as instructions:**
```markdown
Format the code file at $1 using the appropriate formatter...
```

❌ **Don't use generic descriptions:**
```markdown
description: Formats code
```

✅ **Be specific:**
```markdown
description: Format code files using appropriate formatter (black, prettier, etc.)
```

# Plugin Example: Developer Workflow Plugin

This is a working example of a plugin that bundles commands, skills, and hooks for a complete development workflow.

## Plugin Structure

```
dev-workflow/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                 # Slash commands
│   ├── test.md
│   ├── lint.md
│   └── deploy.md
├── skills/                   # Auto-activated skills
│   └── test-generator/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # Pre-commit hooks
├── scripts/
│   ├── run-tests.sh
│   └── lint-check.sh
├── LICENSE
└── README.md
```

## Plugin Manifest

**File**: `.claude-plugin/plugin.json`

```json
{
  "name": "dev-workflow",
  "version": "1.2.0",
  "description": "Complete development workflow with testing, linting, and deployment tools",
  "author": {
    "name": "Dev Team",
    "email": "dev@company.com",
    "url": "https://github.com/company/dev-workflow"
  },
  "homepage": "https://docs.company.com/dev-workflow",
  "repository": "https://github.com/company/dev-workflow-plugin",
  "license": "MIT",
  "keywords": ["development", "testing", "linting", "deployment", "workflow"],
  "hooks": "./hooks/hooks.json"
}
```

### Required Field

Only `"name"` is required. All other fields are optional but recommended.

### Component Paths

The plugin uses default paths:
- `commands/` - Auto-discovered
- `skills/` - Auto-discovered
- `hooks/hooks.json` - Explicitly specified

## Slash Commands

### Test Command

**File**: `commands/test.md`

```markdown
---
description: Run tests with coverage reporting
argument-hint: [test-path]
allowed-tools: Bash, Read, Write
model: haiku
---

# Run Tests

Execute tests at $1 (or all tests if no path specified).

1. Determine test framework:
   - Use Read to check for pytest.ini, jest.config.js, go.mod
2. Run appropriate test command:
   - Python: `pytest $1 --cov --cov-report=html`
   - JavaScript: `npm test -- $1`
   - Go: `go test $1 -cover`
3. Parse results and report:
   - Total tests
   - Pass/fail counts
   - Coverage percentage
4. Use Write to save coverage report summary
```

**Invocation**: `/dev-workflow:test src/auth/`

### Lint Command

**File**: `commands/lint.md`

```markdown
---
description: Check code style and quality issues
argument-hint: [file-or-directory]
allowed-tools: Bash, Read
model: haiku
---

# Lint Code

Run linters on $1 (or entire project if no path specified).

1. Detect file types in target
2. Run appropriate linters:
   - Python: `ruff check $1`
   - JavaScript/TypeScript: `eslint $1`
   - Go: `golangci-lint run $1`
3. Report findings:
   - Group by severity (error, warning, info)
   - Show file:line locations
   - Suggest fixes where available
```

**Invocation**: `/dev-workflow:lint`

## Skills

### Test Generator Skill

**File**: `skills/test-generator/SKILL.md`

```markdown
---
name: test-generator
description: Generates comprehensive test cases for functions and classes. Use when writing tests, improving coverage, or when user mentions testing, test cases, or unit tests.
allowed-tools: Read, Write, Grep
---

# Test Generator

Generate comprehensive test cases following best practices.

## Test Generation Process

1. **Analyze Code**
   - Use Read to examine function/class
   - Identify inputs, outputs, edge cases
   - Understand dependencies

2. **Determine Test Framework**
   - Python: pytest
   - JavaScript: Jest
   - Go: testing package

3. **Generate Tests**
   - Happy path cases
   - Edge cases (null, empty, boundary values)
   - Error conditions
   - Mock external dependencies

4. **Use Write Tool**
   - Create test file (test_*.py, *.test.js, *_test.go)
   - Include setup/teardown if needed

## Test Structure Template

**Python (pytest):**
```python
import pytest
from module import function_name

def test_function_happy_path():
    result = function_name(valid_input)
    assert result == expected_output

def test_function_edge_case_empty():
    with pytest.raises(ValueError):
        function_name("")

def test_function_edge_case_null():
    with pytest.raises(TypeError):
        function_name(None)
```
```

**Activation**: Auto-activates when user says "write tests for this function"

## Hooks Configuration

**File**: `hooks/hooks.json`

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint-check.sh",
          "timeout": 30
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run-tests.sh",
          "timeout": 60
        }
      ]
    }
  ]
}
```

### Pre-commit Lint Hook

Runs before bash commands to ensure code quality.

**File**: `scripts/lint-check.sh`

```bash
#!/bin/bash
set -e

echo "Running pre-commit linting..."

# Detect language and run appropriate linter
if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    ruff check .
elif [ -f "package.json" ]; then
    npm run lint
elif [ -f "go.mod" ]; then
    golangci-lint run
fi

echo "✓ Lint check passed"
```

### Post-write Test Hook

Runs tests after files are written/edited.

**File**: `scripts/run-tests.sh`

```bash
#!/bin/bash
set -e

# Only run if in test mode (env var)
if [ "$RUN_TESTS_ON_WRITE" != "true" ]; then
    exit 0
fi

echo "Running tests after file modification..."

# Detect test framework and run
if [ -f "pytest.ini" ]; then
    pytest --quiet
elif [ -f "jest.config.js" ]; then
    npm test -- --silent
elif [ -f "go.mod" ]; then
    go test ./... -short
fi

echo "✓ Tests passed"
```

## Installation

### Method 1: Clone and Symlink

```bash
# Clone plugin
git clone https://github.com/company/dev-workflow-plugin ~/plugins/dev-workflow

# Install plugin
cd ~/.claude/plugins
ln -s ~/plugins/dev-workflow dev-workflow

# Restart Claude Code
```

### Method 2: Direct Installation

```bash
# Copy to Claude Code plugins directory
cp -r dev-workflow ~/.claude/plugins/

# Restart Claude Code
```

### Method 3: Project-Specific

```bash
# Symlink to project
cd my-project/.claude/plugins
ln -s ~/plugins/dev-workflow dev-workflow

# Plugin only available in this project
```

## Usage

Once installed:

**Commands**:
- `/dev-workflow:test` - Run tests
- `/dev-workflow:lint` - Lint code
- `/dev-workflow:deploy` - Deploy application

**Skills**:
- Say "write tests for this function" → test-generator auto-activates

**Hooks**:
- Pre-commit linting runs automatically
- Tests run after file modifications (if enabled)

## Environment Variables

The plugin uses `${CLAUDE_PLUGIN_ROOT}` for script paths:

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint-check.sh"
}
```

This resolves to the absolute path of the plugin, regardless of where it's installed.

## Key Features

### 1. Namespaced Commands

Commands are prefixed with plugin name:
- `commands/test.md` → `/dev-workflow:test`
- `commands/lint.md` → `/dev-workflow:lint`

### 2. Self-Contained Scripts

All scripts live in the plugin:
```
scripts/
├── run-tests.sh
└── lint-check.sh
```

Referenced via `${CLAUDE_PLUGIN_ROOT}/scripts/...`

### 3. Optional Hook Activation

```bash
if [ "$RUN_TESTS_ON_WRITE" != "true" ]; then
    exit 0
fi
```

Tests only run if user explicitly enables them via environment variable.

### 4. Metadata for Discovery

```json
{
  "keywords": ["development", "testing", "linting", "deployment", "workflow"]
}
```

Helps users find the plugin in a marketplace.

## Best Practices Demonstrated

### ✅ Clear Plugin Purpose

```json
"description": "Complete development workflow with testing, linting, and deployment tools"
```

Users immediately understand what the plugin does.

### ✅ Semantic Versioning

```json
"version": "1.2.0"
```

Follows semver for compatibility tracking.

### ✅ Defensive Hooks

```bash
if [ "$RUN_TESTS_ON_WRITE" != "true" ]; then
    exit 0  # Don't run by default
fi
```

Hooks are opt-in, not forced on users.

### ✅ Portable Paths

```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint-check.sh"
```

Works regardless of installation location.

## Common Mistakes to Avoid

### ❌ Putting Primitives in .claude-plugin/

```
# WRONG
dev-workflow/
├── .claude-plugin/
│   ├── plugin.json
│   ├── commands/        ← WRONG! Should be at root
│   └── skills/          ← WRONG! Should be at root
```

### ✅ Correct Structure

```
# CORRECT
dev-workflow/
├── .claude-plugin/
│   └── plugin.json      ← ONLY plugin.json here
├── commands/            ← At root
└── skills/              ← At root
```

### ❌ Absolute Paths in Config

```json
{
  "command": "/Users/me/plugins/dev-workflow/scripts/test.sh"
}
```

Breaks for other users.

### ✅ Use CLAUDE_PLUGIN_ROOT

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/test.sh"
}
```

### ❌ Missing plugin.json

Without `.claude-plugin/plugin.json`, the directory won't be recognized as a plugin.

## Testing the Plugin

1. **Install plugin**:
   ```bash
   cp -r dev-workflow ~/.claude/plugins/
   ```

2. **Verify installation**:
   ```
   # In Claude Code:
   /dev-workflow:test
   ```

3. **Test skill activation**:
   ```
   Write comprehensive tests for the login() function
   ```

4. **Verify hooks**:
   - Edit a file
   - Check if tests run (if RUN_TESTS_ON_WRITE=true)

## Distribution

### GitHub Release

```bash
# Tag release
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0

# Create release on GitHub
gh release create v1.2.0 --title "v1.2.0" --notes "Release notes"
```

### Plugin Marketplace (Future)

```json
{
  "name": "dev-workflow",
  "repository": "https://github.com/company/dev-workflow-plugin",
  "keywords": ["development", "testing"]
}
```

Users can discover and install via marketplace.

### Private Distribution

For internal/private plugins:

```bash
# Share via git repository
git clone git@github.com:company/internal-dev-workflow.git ~/.claude/plugins/dev-workflow
```

## Updating the Plugin

Users can update via:

```bash
cd ~/.claude/plugins/dev-workflow
git pull origin main
```

Or reinstall from latest release.

## Extension Points

To enhance this plugin:

1. **Add more commands**:
   - `commands/benchmark.md`
   - `commands/profile.md`

2. **Add more skills**:
   - `skills/code-optimizer/`
   - `skills/security-scanner/`

3. **Add MCP server**:
   - `.mcp.json` with CI/CD integration

4. **Add custom output styles**:
   - `outputStyles/test-results.css`

## References

- **Plugin Guide**: https://code.claude.com/docs/en/plugins.md
- **Plugin Reference**: https://code.claude.com/docs/en/plugins-reference.md

# Plugins: Complete Guide

**Metadata for RAG Memory:**
- primitive_type: plugin
- content_type: complete-guide
- version: 1.0

---

## What Are Plugins?

Plugins are **bundled collections of primitives** packaged for distribution and installation. They allow you to share slash commands, skills, subagents, and MCP servers as a single installable unit.

**Key characteristics:**
- **Packaging layer** - Bundles multiple primitives together
- **Distribution mechanism** - Shareable via npm, GitHub, private registries
- **Installation target** - Installs to `.claude/plugins/[plugin-name]/`
- **Versioning** - Semantic versioning for updates
- **Composition** - Contains slash commands, skills, subagents, MCP servers

### Plugins vs Other Primitives

| Feature | Plugins | Skills | Slash Commands |
|---------|---------|--------|----------------|
| Purpose | Package/distribute primitives | Execute workflows | User commands |
| Contains | Other primitives | Instructions + files | Prompt template |
| Distribution | npm, GitHub, private | Files in directory | Files in directory |
| Installation | `claude plugins install` | Manual copy | Manual copy |
| Versioning | Semantic versions | N/A | N/A |
| Updates | Managed updates | Manual | Manual |

---

## When to Use Plugins

Use plugins when:
- **Distributing to team** - Share primitives across organization
- **Reusable across projects** - Same primitives used in multiple projects
- **Versioning needed** - Track updates, manage breaking changes
- **Dependencies required** - Bundle MCP servers with npm/pip dependencies
- **Professional packaging** - Publish for public or private use

Do NOT use plugins when:
- **Personal use only** - Just use `.claude/` or `~/.claude/` directories
- **Single project** - Primitives specific to one project don't need packaging
- **Rapid iteration** - Plugin packaging adds overhead during development

---

## Plugin Structure

```
my-plugin/
  package.json          # Plugin metadata (REQUIRED)
  README.md             # Documentation
  commands/             # Slash commands
    feature-a.md
    feature-b.md
  skills/               # Skills
    skill-a/
      SKILL.md
      supporting-doc.md
    skill-b/
      SKILL.md
  agents/               # Subagents
    specialist-a.md
    specialist-b.md
  servers/              # MCP servers
    my-server/
      __init__.py
      server.py
      requirements.txt
```

---

## package.json Format

### Required Fields

```json
{
  "name": "@company/my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "claudePlugin": {
    "type": "claude-code-plugin",
    "primitives": {
      "commands": ["commands/*.md"],
      "skills": ["skills/*/SKILL.md"],
      "agents": ["agents/*.md"],
      "servers": ["servers/*/"]
    }
  }
}
```

### Field Specifications

**name:** (required, string)
- Package name (scoped or unscoped)
- Scoped: `@org/plugin-name` (recommended for organizations)
- Unscoped: `plugin-name` (public plugins)
- Kebab-case, lowercase
- Example: `@company/devflow-tools`, `github-integration`

**version:** (required, string)
- Semantic version (major.minor.patch)
- Example: `"1.0.0"`, `"2.1.3"`, `"0.1.0-beta"`

**description:** (required, string)
- Brief description of plugin's purpose
- Example: "DevFlow workflow tools for SDLC automation"

**claudePlugin:** (required, object)
- Plugin-specific configuration

**claudePlugin.type:** (required, string)
- Must be `"claude-code-plugin"`

**claudePlugin.primitives:** (required, object)
- Defines which primitives are included
- Uses glob patterns to match files

**claudePlugin.primitives.commands:** (optional, array of globs)
- Slash commands to include
- Example: `["commands/*.md"]`

**claudePlugin.primitives.skills:** (optional, array of globs)
- Skills to include (match SKILL.md files)
- Example: `["skills/*/SKILL.md"]`

**claudePlugin.primitives.agents:** (optional, array of globs)
- Subagents to include
- Example: `["agents/*.md"]`

**claudePlugin.primitives.servers:** (optional, array of globs)
- MCP server directories to include
- Example: `["servers/*/"]`

### Optional Fields

```json
{
  "author": "Your Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/org/repo.git"
  },
  "keywords": ["claude-code", "devflow", "workflow"],
  "dependencies": {
    "some-npm-package": "^1.0.0"
  }
}
```

### Complete Example

```json
{
  "name": "@company/devflow-plugin",
  "version": "1.2.0",
  "description": "DevFlow SDLC workflow automation tools",
  "author": "Engineering Team <eng@company.com>",
  "license": "MIT",
  "keywords": ["claude-code", "sdlc", "workflow", "devflow"],
  "repository": {
    "type": "git",
    "url": "https://github.com/company/devflow-plugin.git"
  },
  "claudePlugin": {
    "type": "claude-code-plugin",
    "primitives": {
      "commands": [
        "commands/*.md"
      ],
      "skills": [
        "skills/*/SKILL.md"
      ],
      "agents": [
        "agents/*.md"
      ],
      "servers": [
        "servers/*/"
      ]
    }
  },
  "dependencies": {
    "mcp-server-sdk": "^0.1.0"
  }
}
```

---

## Installation

### Installing Plugins

**From npm (public):**
```bash
claude plugins install plugin-name
```

**From npm (scoped/private):**
```bash
claude plugins install @company/plugin-name
```

**From GitHub:**
```bash
claude plugins install github:org/repo
```

**From local directory:**
```bash
claude plugins install /path/to/plugin
```

### Where Plugins Install

Plugins install to: `.claude/plugins/[plugin-name]/`

**Example:**
```
.claude/
  plugins/
    devflow-plugin/
      commands/
        plan-work.md
        implement.md
      skills/
        code-reviewer/
          SKILL.md
      agents/
        pattern-analyzer.md
      servers/
        system-monitor/
          server.py
```

### Listing Installed Plugins

```bash
claude plugins list
```

### Updating Plugins

```bash
claude plugins update plugin-name
claude plugins update @company/plugin-name
```

### Uninstalling Plugins

```bash
claude plugins uninstall plugin-name
```

---

## Distribution

### Public Distribution (npm)

**1. Create plugin structure**
```bash
mkdir my-plugin
cd my-plugin
npm init  # Creates package.json
```

**2. Add claudePlugin configuration**
Edit package.json, add claudePlugin section.

**3. Add primitives**
Create commands/, skills/, agents/, servers/ directories.

**4. Test locally**
```bash
claude plugins install .
```

**5. Publish to npm**
```bash
npm publish
```

**Users install:**
```bash
claude plugins install my-plugin
```

### Private Distribution (npm private registry)

**1. Configure npm scope**
```bash
npm config set @company:registry https://npm.company.com
```

**2. Publish scoped package**
```bash
npm publish --access restricted
```

**Users install:**
```bash
npm config set @company:registry https://npm.company.com
claude plugins install @company/plugin-name
```

### GitHub Distribution

**1. Push plugin to GitHub**
```bash
git init
git add .
git commit -m "Initial plugin release"
git tag v1.0.0
git push origin main --tags
```

**Users install:**
```bash
claude plugins install github:org/repo
claude plugins install github:org/repo#v1.0.0  # Specific version
```

### Private GitHub Distribution

**1. Use private repository**
Same as GitHub, but repo is private.

**2. Users need access**
- GitHub token with repo access
- SSH key configured

**Users install:**
```bash
claude plugins install github:org/private-repo
```

---

## Working Examples

### Example 1: DevFlow Plugin

**Directory Structure:**
```
devflow-plugin/
  package.json
  README.md
  commands/
    plan-work.md
    implement.md
    security-review.md
    complete.md
  skills/
    code-reviewer/
      SKILL.md
      quality-checklist.md
  agents/
    pattern-analyzer.md
  servers/
    system-monitor/
      __init__.py
      __main__.py
      server.py
      requirements.txt
```

**package.json:**
```json
{
  "name": "@company/devflow-plugin",
  "version": "1.0.0",
  "description": "DevFlow SDLC workflow automation",
  "claudePlugin": {
    "type": "claude-code-plugin",
    "primitives": {
      "commands": ["commands/*.md"],
      "skills": ["skills/*/SKILL.md"],
      "agents": ["agents/*.md"],
      "servers": ["servers/*/"]
    }
  }
}
```

**Installation:**
```bash
claude plugins install @company/devflow-plugin
```

**Result:**
- `/plan-work`, `/implement`, `/security-review`, `/complete` commands available
- `code-reviewer` skill activates automatically
- `pattern-analyzer` subagent available via Task tool
- `system-monitor` MCP server configured and running

### Example 2: GitHub Integration Plugin

**Directory Structure:**
```
github-plugin/
  package.json
  README.md
  commands/
    create-issue.md
    create-pr.md
    review-pr.md
  servers/
    github-mcp/
      __init__.py
      server.py
      requirements.txt
```

**package.json:**
```json
{
  "name": "github-integration-plugin",
  "version": "2.1.0",
  "description": "GitHub integration tools for Claude Code",
  "keywords": ["github", "git", "pull-request", "issues"],
  "claudePlugin": {
    "type": "claude-code-plugin",
    "primitives": {
      "commands": ["commands/*.md"],
      "servers": ["servers/*/"]
    }
  },
  "dependencies": {
    "mcp-server-sdk": "^0.1.0",
    "requests": "^2.31.0"
  }
}
```

**commands/create-issue.md:**
```markdown
---
description: Create GitHub issue from current context
allowed-tools: [mcp__github-mcp__create_issue, Bash]
---

Create a GitHub issue:

1. Get repo: `git remote get-url origin`
2. Ask user for issue details
3. Call mcp__github-mcp__create_issue
4. Show created issue URL
```

**Installation:**
```bash
claude plugins install github-integration-plugin
```

### Example 3: Security Review Plugin

**Directory Structure:**
```
security-plugin/
  package.json
  README.md
  commands/
    security-scan.md
  skills/
    security-reviewer/
      SKILL.md
      owasp-checklist.md
      threat-model.md
  agents/
    vulnerability-analyzer.md
```

**package.json:**
```json
{
  "name": "@security-team/security-plugin",
  "version": "3.0.0",
  "description": "Security analysis and review tools",
  "claudePlugin": {
    "type": "claude-code-plugin",
    "primitives": {
      "commands": ["commands/*.md"],
      "skills": ["skills/*/SKILL.md"],
      "agents": ["agents/*.md"]
    }
  }
}
```

**Private distribution (GitHub):**
```bash
# Publish
git tag v3.0.0
git push origin main --tags

# Users install
claude plugins install github:security-team/security-plugin
```

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Packaging Personal Preferences

**WRONG:** Creating plugin for your personal code style preferences

**Why it's wrong:** Plugins are for SHARING. Personal preferences go in `~/.claude/`.

**RIGHT:** Keep personal primitives in `~/.claude/`, only create plugins for team-shared tools.

### ❌ Anti-Pattern 2: Missing Version Management

**WRONG:** Never updating version in package.json

**Why it's wrong:** Users can't track updates, breaking changes surprise them.

**RIGHT:** Use semantic versioning:
- Major (1.0.0 → 2.0.0): Breaking changes
- Minor (1.0.0 → 1.1.0): New features, backward compatible
- Patch (1.0.0 → 1.0.1): Bug fixes

### ❌ Anti-Pattern 3: Monolithic Plugin

**WRONG:** One giant plugin with unrelated primitives

**Why it's wrong:** Users forced to install everything, can't pick what they need.

**RIGHT:** Create focused plugins by domain:
- `@company/github-tools` - GitHub integration
- `@company/devflow-tools` - SDLC workflow
- `@company/security-tools` - Security review

### ❌ Anti-Pattern 4: No Documentation

**WRONG:** Plugin with no README explaining what it does or how to configure it

**Why it's wrong:** Users don't know what they're installing or how to use it.

**RIGHT:** Include comprehensive README:
- What the plugin does
- What primitives it provides
- Configuration requirements (API keys, etc.)
- Usage examples

### ❌ Anti-Pattern 5: Hardcoded Configuration

**WRONG:** MCP servers in plugin with hardcoded URLs/credentials

**Why it's wrong:** Users can't configure for their environment.

**RIGHT:** Use environment variables in MCP server, document in README:
```markdown
## Configuration

After installing, configure API credentials:

1. Edit `.claude/settings.json`
2. Add to mcpServers.github-mcp.env:
   - GITHUB_TOKEN: Your GitHub personal access token
   - GITHUB_API_URL: https://api.github.com (or enterprise URL)
```

---

## Versioning Best Practices

### Semantic Versioning

**Major version (X.0.0):** Breaking changes
- Removed primitives
- Changed primitive names
- Changed required parameters
- Changed behavior significantly

**Minor version (0.X.0):** New features, backward compatible
- New primitives added
- New optional parameters
- Enhanced existing features

**Patch version (0.0.X):** Bug fixes
- Fixed bugs
- Documentation updates
- Performance improvements

### Changelog

Maintain CHANGELOG.md:

```markdown
# Changelog

## [2.0.0] - 2024-01-15
### Breaking Changes
- Renamed `/create-issue` to `/github-issue` for clarity
- Removed deprecated `/old-command`

### Added
- New `/create-pr` command for pull request creation
- `pr-reviewer` skill for automated PR reviews

## [1.1.0] - 2024-01-01
### Added
- `/list-issues` command
- GitHub label management

### Fixed
- Issue creation error handling
```

---

## Configuration Requirements

### Document Required Configuration

In README.md:

```markdown
## Installation

```bash
claude plugins install @company/devflow-plugin
```

## Configuration

### 1. MCP Server Credentials

Edit `.claude/settings.json` and add:

```json
{
  "mcpServers": {
    "system-monitor": {
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### 2. Get JIRA API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create API token
3. Copy to configuration above

## Usage

After configuration, use these commands:
- `/plan-work` - Plan implementation from JIRA issue
- `/implement` - TDD implementation with gates
- `/complete` - Finish workflow and create PR
```

---

## Testing Plugins

### Before Publishing

**1. Test local installation:**
```bash
cd my-plugin
claude plugins install .
```

**2. Verify primitives work:**
- Try each slash command
- Trigger each skill
- Invoke each subagent
- Test MCP server tools

**3. Test in clean environment:**
```bash
# In different project
claude plugins install /path/to/my-plugin
# Verify everything works without project-specific config
```

**4. Test updates:**
```bash
# Bump version in package.json
claude plugins update my-plugin
# Verify update applies correctly
```

### After Publishing

**1. Install from registry:**
```bash
# Fresh install
claude plugins install my-plugin
```

**2. Test documentation:**
- Follow README instructions
- Verify configuration steps work
- Check all examples execute correctly

**3. Get feedback:**
- Have colleague install and test
- Address issues before next version

---

## Summary Checklist

When creating a plugin, verify:

- [ ] package.json has all required fields (name, version, description, claudePlugin)
- [ ] claudePlugin.type is "claude-code-plugin"
- [ ] claudePlugin.primitives lists all primitive types included
- [ ] Version follows semantic versioning (major.minor.patch)
- [ ] README.md documents:
  - What plugin does
  - Installation instructions
  - Configuration requirements
  - Usage examples
- [ ] CHANGELOG.md tracks versions and changes
- [ ] MCP servers use environment variables (no hardcoded config)
- [ ] All primitives tested individually
- [ ] Plugin tested via local installation
- [ ] Plugin tested in clean environment
- [ ] Distribution method chosen (npm, GitHub, private)
- [ ] License specified if public distribution
- [ ] Keywords added for discoverability

---

## Reference

**Official Claude Code Plugins Documentation:**
- [Plugins Guide](https://docs.anthropic.com/claude/docs/plugins)
- [Publishing Plugins](https://docs.anthropic.com/claude/docs/publishing-plugins)

**Package Format:** npm package.json with claudePlugin section

**Installation Command:** `claude plugins install [package]`

**Installation Location:** `.claude/plugins/[plugin-name]/`

**Distribution:** npm (public/private), GitHub (public/private), local filesystem

**Versioning:** Semantic versioning (major.minor.patch)

**Primitive Types:** commands, skills, agents, servers

**Required Fields:** name, version, description, claudePlugin.type, claudePlugin.primitives

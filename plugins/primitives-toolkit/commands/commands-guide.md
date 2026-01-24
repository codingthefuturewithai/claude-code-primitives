---
description: Discover all available custom slash commands with descriptions and usage
argument-hint: "[category]"
allowed-tools: ["Bash", "Read", "Glob"]
---

# Custom Slash Commands Guide

**Request:** $ARGUMENTS

---

## Step 1: Discover Available Commands

Scan the `.claude/commands/` directory to find all available commands and categories.

```
[Use Glob to find all .md files in .claude/commands/ and subdirectories]
[Pattern: .claude/commands/**/*.md]
[Exclude this file: commands-guide.md]
```

---

## Step 2: Extract Command Information

For each `.md` file found, read the YAML frontmatter to extract:
- **description** - What the command does
- **argument-hint** - How to invoke it with arguments

```
[Read the first 10 lines of each file to get frontmatter]
[Parse: description, argument-hint fields]
[Derive command name from file path: folder:filename (without .md)]
```

---

## Step 3: Organize by Category

Group commands by their folder (category):
- Files in `.claude/commands/*.md` → Root level commands
- Files in `.claude/commands/[folder]/*.md` → Category: [folder]

**Known categories:** devflow, pm, infra, onboarding, support, docs, features
**Note:** If new folders exist, include them automatically.

---

## Step 4: Handle Arguments

**If $ARGUMENTS is empty:**
Show ALL commands organized by category.

**If $ARGUMENTS matches a category name:**
Show only commands in that category.

**If $ARGUMENTS is "categories" or "list":**
Show just the category names and command counts.

**If $ARGUMENTS doesn't match a known category:**
Say: "Unknown category '[argument]'. Here are available categories: [list discovered categories]"

---

## Step 5: Present Results

### Format for Each Command:

```
`/[category]:[command-name]` [argument-hint if any]
  [description from frontmatter]
```

### Format for Category Summary:

```
## [Category Name] ([count] commands)

[Brief description of what this category covers based on the commands within]

| Command | Description |
|---------|-------------|
| `/category:command` | Description from frontmatter |
```

---

## Step 6: Provide Summary

At the end, provide:
1. Total command count across all categories
2. Brief summary of capabilities (1-2 sentences per category)
3. Tip: "Use `/commands-guide [category]` to see details for a specific category"

---

## Rules

**Always:**
- Scan the actual directory structure (don't assume what exists)
- Read frontmatter from each command file
- Include any new folders/commands automatically
- Show argument-hint if the command accepts arguments

**Never:**
- Hardcode command lists (they will become stale)
- Skip commands missing from a predefined list
- Assume folder structure hasn't changed

---

## Example Output

```
## Custom Slash Commands

### devflow (8 commands)
Development workflow - JIRA-integrated development lifecycle

| Command | Description |
|---------|-------------|
| `/devflow:fetch-issue [KEY]` | Fetch JIRA issue and analyze feasibility |
| `/devflow:plan-work [KEY]` | Analyze JIRA issue and develop implementation plan |
...

### pm (2 commands)
Product management - Confluence and JIRA planning

| Command | Description |
|---------|-------------|
| `/pm:roadmap [mode]` | Manage Confluence Product Planning & Roadmap |
| `/pm:backlog [mode]` | Manage JIRA backlog from Confluence roadmap |

...

---

**Total: X commands across Y categories**

Tip: Use `/commands-guide [category]` to focus on a specific category.
```

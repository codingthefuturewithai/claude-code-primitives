#!/usr/bin/env python3
"""
Discover all DevFlow plugin primitives: skills, sub-agents, hooks, and commands.
Outputs structured JSON for Claude to format and present.
"""
import json
import os
import re
import sys
from pathlib import Path


def find_plugin_path():
    """Find the devflow plugin path (cache or source repo)."""
    # Check plugin cache first
    cache_base = Path.home() / ".claude/plugins/cache/claude-code-primitives"
    if cache_base.exists():
        for version_dir in cache_base.glob("devflow/*"):
            if version_dir.is_dir() and (version_dir / "skills").exists():
                return version_dir

    # Check if we're in the source repo
    cwd = Path.cwd()
    source_plugin = cwd / "plugins/devflow"
    if source_plugin.exists():
        return source_plugin

    # Check parent directories for source repo
    for parent in cwd.parents:
        source_plugin = parent / "plugins/devflow"
        if source_plugin.exists():
            return source_plugin

    return None


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Handle booleans
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter


def discover_skills(plugin_path):
    """Discover all skills and sub-agents."""
    skills = []
    skills_dir = plugin_path / "skills"

    if not skills_dir.exists():
        return skills

    for skill_link in skills_dir.iterdir():
        # Follow symlinks to find SKILL.md
        skill_path = skill_link
        if skill_link.is_symlink():
            skill_path = skill_link.resolve()

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            # Try the symlink target directly
            skill_md = skill_link / "SKILL.md"
            if not skill_md.exists():
                continue

        try:
            content = skill_md.read_text()
            fm = parse_frontmatter(content)

            skill_info = {
                "directory": skill_link.name,
                "name": fm.get("name", skill_link.name),
                "description": fm.get("description", "No description"),
                "is_subagent": fm.get("context") == "fork",
                "agent_type": fm.get("agent", None),
                "user_invocable": fm.get("user-invocable", True),
                "disable_model_invocation": fm.get("disable-model-invocation", False),
            }

            # Categorize by directory prefix
            dir_name = skill_link.name
            if dir_name.startswith("build-"):
                skill_info["category"] = "build"
            elif dir_name.startswith("pm-"):
                skill_info["category"] = "pm"
            elif dir_name.startswith("docs-"):
                skill_info["category"] = "docs"
            elif dir_name.startswith("rag-memory-"):
                skill_info["category"] = "rag-memory"
            elif dir_name.startswith("devops-"):
                skill_info["category"] = "devops"
            else:
                skill_info["category"] = "core"

            skills.append(skill_info)
        except Exception as e:
            # Skip skills that can't be read
            continue

    return skills


def discover_hooks(plugin_path):
    """Discover all hook scripts."""
    hooks = []
    hooks_dir = plugin_path / "hooks"

    if not hooks_dir.exists():
        return hooks

    hook_descriptions = {
        "atlassian-approval.py": "Jira and Confluence operations",
        "gitlab-approval.py": "GitLab issues and merge requests",
        "google-workspace-approval.py": "Google Docs and Drive",
        "rag-memory-approval.py": "RAG Memory operations",
    }

    for hook_file in hooks_dir.glob("*.py"):
        hook_info = {
            "name": hook_file.name,
            "protects": hook_descriptions.get(hook_file.name, "Unknown operations"),
        }
        hooks.append(hook_info)

    return hooks


def discover_commands(plugin_path):
    """Discover traditional commands if any exist."""
    commands = []
    commands_dir = plugin_path / "commands"

    if not commands_dir.exists():
        return commands

    for cmd_file in commands_dir.glob("**/*.md"):
        try:
            content = cmd_file.read_text()
            fm = parse_frontmatter(content)

            cmd_info = {
                "name": fm.get("name", cmd_file.stem),
                "description": fm.get("description", "No description"),
            }
            commands.append(cmd_info)
        except Exception:
            continue

    return commands


def main():
    plugin_path = find_plugin_path()

    if not plugin_path:
        print(json.dumps({
            "error": "Could not find DevFlow plugin",
            "searched": [
                "~/.claude/plugins/cache/claude-code-primitives/devflow/*/",
                "plugins/devflow/"
            ]
        }, indent=2))
        sys.exit(1)

    result = {
        "plugin_path": str(plugin_path),
        "skills": discover_skills(plugin_path),
        "hooks": discover_hooks(plugin_path),
        "commands": discover_commands(plugin_path),
    }

    # Add summary counts
    result["summary"] = {
        "total_skills": len(result["skills"]),
        "subagents": len([s for s in result["skills"] if s["is_subagent"]]),
        "hooks": len(result["hooks"]),
        "commands": len(result["commands"]),
    }

    # Group skills by category
    categories = {}
    for skill in result["skills"]:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)
    result["by_category"] = categories

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

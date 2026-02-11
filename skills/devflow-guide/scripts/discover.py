#!/usr/bin/env python3
"""
Discover all DevFlow plugin primitives: skills, agents, hooks, and commands.
Outputs structured JSON for Claude to format and present.

Runs within the installed plugin context only. The plugin root is passed
as a CLI argument (${CLAUDE_PLUGIN_ROOT}) or derived from this script's location.
"""
import json
import re
import sys
from pathlib import Path


def get_plugin_root():
    """Get the plugin root directory."""
    # Prefer CLI argument (passed as ${CLAUDE_PLUGIN_ROOT} from SKILL.md)
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
        if root.exists():
            return root

    # Fallback: derive from this script's location
    # Script is at: <plugin_root>/skills/devflow-guide/scripts/discover.py
    return Path(__file__).resolve().parent.parent.parent.parent


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter


def discover_skills(plugin_root):
    """Discover all skills from the plugin's skills/ directory."""
    skills = []
    skills_dir = plugin_root / "skills"

    if not skills_dir.exists():
        return skills

    for entry in skills_dir.iterdir():
        if entry.name.startswith('.'):
            continue

        # Find SKILL.md in the entry (follow symlinks transparently)
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text()
            fm = parse_frontmatter(content)

            skill_info = {
                "directory": entry.name,
                "name": fm.get("name", entry.name),
                "description": fm.get("description", "No description"),
                "is_subagent": fm.get("context") == "fork",
                "agent_type": fm.get("agent", None),
                "user_invocable": fm.get("user-invocable", True),
                "disable_model_invocation": fm.get("disable-model-invocation", False),
            }

            # Categorize by directory prefix
            # Installed plugins flatten nested dirs: build/complete-issue -> build-complete-issue
            dir_name = entry.name
            if dir_name.startswith("build"):
                skill_info["category"] = "build"
            elif dir_name.startswith("pm"):
                skill_info["category"] = "pm"
            elif dir_name.startswith("docs"):
                skill_info["category"] = "docs"
            elif dir_name.startswith("rag-memory"):
                skill_info["category"] = "rag-memory"
            elif dir_name.startswith("devops"):
                skill_info["category"] = "devops"
            elif dir_name.startswith("foundation"):
                skill_info["category"] = "foundation"
            else:
                skill_info["category"] = "core"

            skills.append(skill_info)
        except Exception:
            continue

    return sorted(skills, key=lambda s: (s["category"], s["name"]))


def discover_agents(plugin_root):
    """Discover all custom agents from the plugin's agents/ directory."""
    agents = []
    agents_dir = plugin_root / "agents"

    if not agents_dir.exists():
        return agents

    for entry in agents_dir.iterdir():
        if entry.name.startswith('.'):
            continue

        # Agent definitions are .md files
        agent_file = entry
        if entry.is_dir():
            candidate = entry / "agent.md"
            if candidate.exists():
                agent_file = candidate
            else:
                continue
        elif not entry.suffix == '.md':
            continue

        try:
            content = agent_file.read_text()
            fm = parse_frontmatter(content)

            agent_info = {
                "name": fm.get("name", entry.stem),
                "description": fm.get("description", "No description"),
                "model": fm.get("model", "default"),
            }

            # Extract tools list from frontmatter
            tools_match = re.search(r'^tools:\s*\n((?:\s+-\s+.*\n)*)', content, re.MULTILINE)
            if tools_match:
                agent_info["tools"] = [
                    t.strip().lstrip('- ') for t in tools_match.group(1).strip().split('\n')
                    if t.strip()
                ]

            agents.append(agent_info)
        except Exception:
            continue

    return sorted(agents, key=lambda a: a["name"])


def discover_hooks(plugin_root):
    """Discover hooks from hooks.json and hook scripts."""
    hooks_dir = plugin_root / "hooks"
    result = {
        "scripts": [],
        "matchers": [],
    }

    if not hooks_dir.exists():
        return result

    # Discover hook scripts
    hook_descriptions = {
        "atlassian-approval.py": "Jira and Confluence write operations",
        "gitlab-approval.py": "GitLab issues and merge requests",
        "google-drive-approval.py": "Google Drive file operations",
        "rag-memory-approval.py": "RAG Memory write operations",
    }

    for hook_file in hooks_dir.glob("*.py"):
        result["scripts"].append({
            "name": hook_file.name,
            "protects": hook_descriptions.get(hook_file.name, "Unknown operations"),
        })

    # Parse hooks.json for active matchers
    hooks_json = hooks_dir / "hooks.json"
    if hooks_json.exists():
        try:
            data = json.loads(hooks_json.read_text())
            for event, matcher_list in data.get("hooks", {}).items():
                for matcher_entry in matcher_list:
                    matcher_pattern = matcher_entry.get("matcher", "")
                    for hook in matcher_entry.get("hooks", []):
                        command = hook.get("command", "")
                        script_name = command.split("/")[-1] if "/" in command else command
                        result["matchers"].append({
                            "event": event,
                            "matcher": matcher_pattern,
                            "script": script_name,
                            "type": hook.get("type", "command"),
                        })
        except Exception:
            pass

    # Group matchers by backend
    backend_groups = {}
    for m in result["matchers"]:
        pattern = m["matcher"]
        if "rag-memory" in pattern:
            backend = "RAG Memory"
        elif "atlassian" in pattern:
            backend = "Atlassian"
        elif "google-drive" in pattern:
            backend = "Google Drive"
        elif "gitlab" in pattern:
            backend = "GitLab"
        else:
            backend = "Other"

        if backend not in backend_groups:
            backend_groups[backend] = []
        op = pattern.split("__")[-1] if "__" in pattern else pattern
        if op not in [x["operation"] for x in backend_groups[backend]]:
            backend_groups[backend].append({
                "operation": op,
                "matcher": pattern,
            })

    result["by_backend"] = backend_groups
    return result


def discover_commands(plugin_root):
    """Discover traditional commands if any exist."""
    commands = []
    commands_dir = plugin_root / "commands"

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
    plugin_root = get_plugin_root()

    if not plugin_root.exists():
        print(json.dumps({
            "error": "Plugin root not found",
            "path": str(plugin_root),
            "hint": "Pass ${CLAUDE_PLUGIN_ROOT} as argument"
        }, indent=2))
        sys.exit(1)

    result = {
        "plugin_path": str(plugin_root),
        "skills": discover_skills(plugin_root),
        "agents": discover_agents(plugin_root),
        "hooks": discover_hooks(plugin_root),
        "commands": discover_commands(plugin_root),
    }

    result["summary"] = {
        "total_skills": len(result["skills"]),
        "subagents": len([s for s in result["skills"] if s["is_subagent"]]),
        "custom_agents": len(result["agents"]),
        "hook_scripts": len(result["hooks"]["scripts"]),
        "protected_operations": len(result["hooks"]["matchers"]),
        "commands": len(result["commands"]),
    }

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

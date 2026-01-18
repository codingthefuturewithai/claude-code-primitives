#!/usr/bin/env python3
"""
Setup script to create symlinks for plugin skills.

Workaround for Claude Code bug where plugin skills are not injected into
the available_skills context. This script creates symlinks from the plugin's
skills directory to ~/.claude/skills/ so they load properly.

Usage:
    python setup-skills.py          # Auto-detect plugin location
    python setup-skills.py --check  # Check status only, don't create
    python setup-skills.py --remove # Remove symlinks created by this script
"""

import argparse
import json
import os
import sys
from pathlib import Path


def get_claude_skills_dir() -> Path:
    """Get the user's Claude skills directory."""
    return Path.home() / ".claude" / "skills"


def get_installed_plugin_path() -> Path | None:
    """Find the installed plugin path from Claude's plugin registry."""
    installed_plugins_file = Path.home() / ".claude" / "plugins" / "installed_plugins.json"

    if not installed_plugins_file.exists():
        return None

    try:
        with open(installed_plugins_file) as f:
            data = json.load(f)

        plugins = data.get("plugins", {})
        for key, installs in plugins.items():
            if "primitives-toolkit" in key:
                if installs and len(installs) > 0:
                    return Path(installs[0].get("installPath", ""))
        return None
    except (json.JSONDecodeError, KeyError):
        return None


def get_plugin_skills(plugin_path: Path) -> list[Path]:
    """Get all skill directories from the plugin."""
    skills_dir = plugin_path / "skills"
    if not skills_dir.exists():
        return []

    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item)
    return skills


def check_symlink(skill_name: str, target_path: Path, claude_skills_dir: Path) -> dict:
    """Check the status of a skill symlink."""
    link_path = claude_skills_dir / skill_name

    result = {
        "name": skill_name,
        "link_path": str(link_path),
        "target_path": str(target_path),
        "status": "missing",
        "current_target": None
    }

    if link_path.exists() or link_path.is_symlink():
        if link_path.is_symlink():
            current_target = os.readlink(link_path)
            result["current_target"] = current_target

            if Path(current_target).resolve() == target_path.resolve():
                result["status"] = "ok"
            else:
                result["status"] = "wrong_target"
        else:
            result["status"] = "not_symlink"

    return result


def create_symlink(skill_name: str, target_path: Path, claude_skills_dir: Path, force: bool = False) -> bool:
    """Create a symlink for a skill."""
    link_path = claude_skills_dir / skill_name

    # Ensure skills directory exists
    claude_skills_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing if force
    if link_path.exists() or link_path.is_symlink():
        if force:
            if link_path.is_symlink():
                link_path.unlink()
            else:
                print(f"  ⚠️  {skill_name}: Not a symlink, skipping (use manual removal)")
                return False
        else:
            return False

    # Create symlink
    link_path.symlink_to(target_path)
    return True


def remove_symlink(skill_name: str, claude_skills_dir: Path) -> bool:
    """Remove a skill symlink if it points to our plugin."""
    link_path = claude_skills_dir / skill_name

    if link_path.is_symlink():
        target = os.readlink(link_path)
        if "primitives-toolkit" in target:
            link_path.unlink()
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Setup symlinks for primitives-toolkit skills")
    parser.add_argument("--check", action="store_true", help="Check status only, don't create symlinks")
    parser.add_argument("--remove", action="store_true", help="Remove symlinks created by this script")
    parser.add_argument("--plugin-path", type=str, help="Override plugin path (auto-detected by default)")
    args = parser.parse_args()

    # Find plugin path
    if args.plugin_path:
        plugin_path = Path(args.plugin_path)
    else:
        # First try: script is inside the plugin
        script_dir = Path(__file__).parent
        if (script_dir.parent / "skills").exists():
            plugin_path = script_dir.parent
        else:
            # Second try: find from installed plugins
            plugin_path = get_installed_plugin_path()

    if not plugin_path or not plugin_path.exists():
        print("❌ Could not find plugin path. Use --plugin-path to specify.")
        sys.exit(1)

    print(f"📦 Plugin path: {plugin_path}")

    claude_skills_dir = get_claude_skills_dir()
    print(f"📁 Skills directory: {claude_skills_dir}")

    skills = get_plugin_skills(plugin_path)
    if not skills:
        print("❌ No skills found in plugin")
        sys.exit(1)

    print(f"🔍 Found {len(skills)} skills: {', '.join(s.name for s in skills)}\n")

    if args.remove:
        print("🗑️  Removing symlinks...\n")
        for skill_path in skills:
            skill_name = skill_path.name
            if remove_symlink(skill_name, claude_skills_dir):
                print(f"  ✅ {skill_name}: Removed")
            else:
                print(f"  ⏭️  {skill_name}: Not a symlink to our plugin, skipped")
        print("\n✨ Done!")
        return

    # Check or create
    all_ok = True
    for skill_path in skills:
        skill_name = skill_path.name
        status = check_symlink(skill_name, skill_path, claude_skills_dir)

        if status["status"] == "ok":
            print(f"  ✅ {skill_name}: OK")
        elif status["status"] == "missing":
            if args.check:
                print(f"  ❌ {skill_name}: Missing")
                all_ok = False
            else:
                if create_symlink(skill_name, skill_path, claude_skills_dir):
                    print(f"  ✅ {skill_name}: Created")
                else:
                    print(f"  ❌ {skill_name}: Failed to create")
                    all_ok = False
        elif status["status"] == "wrong_target":
            if args.check:
                print(f"  ⚠️  {skill_name}: Wrong target -> {status['current_target']}")
                all_ok = False
            else:
                if create_symlink(skill_name, skill_path, claude_skills_dir, force=True):
                    print(f"  ✅ {skill_name}: Updated (was pointing elsewhere)")
                else:
                    print(f"  ❌ {skill_name}: Failed to update")
                    all_ok = False
        elif status["status"] == "not_symlink":
            print(f"  ⚠️  {skill_name}: Exists but not a symlink (manual removal needed)")
            all_ok = False

    print()
    if all_ok:
        print("✨ All skills are set up! Restart Claude Code to use them.")
    else:
        if args.check:
            print("❌ Some skills need setup. Run without --check to fix.")
        else:
            print("⚠️  Some skills could not be set up. Check messages above.")


if __name__ == "__main__":
    main()

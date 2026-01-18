---
name: setup
description: Set up plugin skills by creating necessary symlinks. Run this once after installing the plugin.
---

# Plugin Setup Command

Run the appropriate setup script based on the operating system to create symlinks for plugin skills.

## Instructions

1. First, detect the operating system by running:
```bash
uname -s 2>/dev/null || echo "Windows"
```

2. Based on the OS, execute the setup:

### For macOS or Linux (Darwin or Linux):

```bash
#!/bin/bash
set -e

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
PLUGIN_SKILLS_DIR="${CLAUDE_PLUGIN_ROOT}/skills"

echo "🔧 primitives-toolkit Setup"
echo "=========================="
echo ""
echo "📁 Plugin skills: $PLUGIN_SKILLS_DIR"
echo "📁 User skills: $CLAUDE_SKILLS_DIR"
echo ""

# Create skills directory if needed
mkdir -p "$CLAUDE_SKILLS_DIR"

# Find all skills and create symlinks
for skill_dir in "$PLUGIN_SKILLS_DIR"/*/; do
    if [ -f "${skill_dir}SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        link_path="$CLAUDE_SKILLS_DIR/$skill_name"
        target_path="$PLUGIN_SKILLS_DIR/$skill_name"

        if [ -L "$link_path" ]; then
            current_target=$(readlink "$link_path")
            if [ "$current_target" = "$target_path" ]; then
                echo "✅ $skill_name: Already configured"
            else
                rm "$link_path"
                ln -s "$target_path" "$link_path"
                echo "✅ $skill_name: Updated symlink"
            fi
        elif [ -e "$link_path" ]; then
            echo "⚠️  $skill_name: Exists but not a symlink (skipped)"
        else
            ln -s "$target_path" "$link_path"
            echo "✅ $skill_name: Created symlink"
        fi
    fi
done

echo ""
echo "✨ Setup complete! Start a new Claude Code session to use the skills."
```

### For Windows (PowerShell):

```powershell
$ErrorActionPreference = "Stop"

$claudeSkillsDir = "$env:USERPROFILE\.claude\skills"
$pluginSkillsDir = "$env:CLAUDE_PLUGIN_ROOT\skills"

Write-Host "🔧 primitives-toolkit Setup" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Plugin skills: $pluginSkillsDir"
Write-Host "📁 User skills: $claudeSkillsDir"
Write-Host ""

# Create skills directory if needed
if (!(Test-Path $claudeSkillsDir)) {
    New-Item -ItemType Directory -Path $claudeSkillsDir -Force | Out-Null
}

# Find all skills and create symlinks
Get-ChildItem -Path $pluginSkillsDir -Directory | ForEach-Object {
    $skillName = $_.Name
    $skillPath = $_.FullName
    $linkPath = Join-Path $claudeSkillsDir $skillName

    if (Test-Path (Join-Path $skillPath "SKILL.md")) {
        if (Test-Path $linkPath) {
            $item = Get-Item $linkPath -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                # It's a symlink/junction
                $currentTarget = (Get-Item $linkPath).Target
                if ($currentTarget -eq $skillPath) {
                    Write-Host "✅ ${skillName}: Already configured" -ForegroundColor Green
                } else {
                    Remove-Item $linkPath -Force
                    New-Item -ItemType SymbolicLink -Path $linkPath -Target $skillPath -Force | Out-Null
                    Write-Host "✅ ${skillName}: Updated symlink" -ForegroundColor Green
                }
            } else {
                Write-Host "⚠️  ${skillName}: Exists but not a symlink (skipped)" -ForegroundColor Yellow
            }
        } else {
            New-Item -ItemType SymbolicLink -Path $linkPath -Target $skillPath -Force | Out-Null
            Write-Host "✅ ${skillName}: Created symlink" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "✨ Setup complete! Start a new Claude Code session to use the skills." -ForegroundColor Green
```

3. After running the setup, verify by listing the skills directory:

**macOS/Linux:**
```bash
ls -la "$HOME/.claude/skills/"
```

**Windows:**
```powershell
Get-ChildItem "$env:USERPROFILE\.claude\skills" | Format-Table Name, LinkType, Target
```

4. Tell the user: "Setup complete! Please start a new Claude Code session. Your skills will now appear when you type `/` in the prompt."

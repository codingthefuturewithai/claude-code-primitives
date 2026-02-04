# GitHub VCS Operations (Pull Requests)

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Verify: `which gh && gh auth status`

If not available, STOP and inform user.

---

## Operations

### Create Pull Request

```bash
gh pr create --title "[ISSUE-KEY]: [Summary]" --body "$(cat <<'EOF'
Fixes [ISSUE-REF]

## Summary
[What was implemented and why]

## Changes
- [Key change 1]
- [Key change 2]

## Validation
- Tests: [X passed]
- Coverage: [Y%]

**Issue:** [link to issue]
EOF
)"
```

Parameters:
- `--title`: [FROM: issue key from user input + issue summary from issue tracker response. NEVER fabricate.]
- `--body`: [FROM: generated from change analysis. OK to construct.]
- `[ISSUE-KEY]` in body: [FROM: user input `$ARGUMENTS`. NEVER construct.]
- `[ISSUE-REF]` in body: [FROM: user input. For GitHub issues use `#NUMBER`. NEVER fabricate.]

**Optional flags:**
- `--base main`: [FROM: git branch context or config. OK to use default.]
- `--head feature-branch`: [FROM: current git branch. `git branch --show-current`.]
- `--draft`: [FROM: user request]
- `--assignee @me`: [FROM: user request]
- `--reviewer user1,user2`: [FROM: user request. NEVER guess reviewers.]

---

### View Pull Request

```bash
gh pr view [PR_NUMBER]
```

- `[PR_NUMBER]`: [FROM: `gh pr create` response or user input. NEVER guess.]

```bash
gh pr view --web  # Open in browser
```

---

### List Pull Requests

```bash
gh pr list
gh pr list --state open
gh pr list --author @me
```

---

### Check PR Status

```bash
gh pr status
gh pr checks [PR_NUMBER]
```

- `[PR_NUMBER]`: [FROM: `gh pr create` response or user input. NEVER guess.]

---

### Merge Pull Request

```bash
gh pr merge [PR_NUMBER] --merge   # Merge commit
gh pr merge [PR_NUMBER] --squash  # Squash and merge
gh pr merge [PR_NUMBER] --rebase  # Rebase and merge
```

- `[PR_NUMBER]`: [FROM: `gh pr create` response or user input. NEVER guess.]

---

### Create Branch

```bash
git checkout -b [BRANCH_NAME]
git push -u origin [BRANCH_NAME]
```

- `[BRANCH_NAME]`: [FROM: constructed from issue key + description slug. OK to construct from user input.]

Branch naming convention:
- Feature: `feature/[ISSUE-KEY]-[slug]`
- Bug fix: `bugfix/[ISSUE-KEY]-[slug]`
- Other: `task/[ISSUE-KEY]-[slug]`

---

## PR Body Template

Standard format for DevFlow:

```markdown
Fixes [ISSUE-REF]

## Summary
[1-3 sentences describing what was done]

## Changes
- [File/component]: [What changed]

## Validation
[How the changes were tested]
- Tests: [X passed, Y failed]
- Coverage: [Z%] (if applicable)

## Related
- Issue: [link]
- Docs: [link if applicable]
```

---

## Post-Merge Cleanup

```bash
git checkout main
git pull
git branch -d [BRANCH_NAME]
git push origin --delete [BRANCH_NAME]
```

- `[BRANCH_NAME]`: [FROM: `git branch --show-current` before switching. NEVER guess.]

---

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| "not a git repository" | Not in git repo | cd to repo root |
| "authentication required" | Not logged in | `gh auth login` |
| "no upstream branch" | Branch not pushed | `git push -u origin branch` |
| "merge conflicts" | Conflicts exist | Resolve conflicts first |

---

## Parameter Sources

| Parameter | Authorized Source | NEVER |
|-----------|------------------|-------|
| PR title | Issue key (user input) + issue summary (tracker response) | Fabricate |
| PR body | Generated from change analysis | N/A (content, not identifier) |
| base branch | Git context or config | Assume without checking |
| head branch | `git branch --show-current` | Guess |
| PR number | `gh pr create` response | Fabricate |
| reviewer usernames | User input | Guess or infer |

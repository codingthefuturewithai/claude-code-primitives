# GitHub Issues — Detection & Setup

## Step 1: Detection

Test gh CLI availability:
```bash
which gh
```

Then test authentication:
```bash
gh auth status
```

---

## If Detection Succeeds (both pass)

> "GitHub CLI detected and authenticated."

Store:
- `ISSUES_BACKEND = "github"`
- `ISSUES_ENABLED = true`

Return to SKILL.md for next step.

---

## If Detection Fails

### gh not installed

> "GitHub CLI (gh) not installed. Install it:"
>
> - **macOS:** `brew install gh`
> - **Linux:** See https://github.com/cli/cli#installation
> - **Windows:** `winget install GitHub.cli`
>
> After installing, authenticate: `gh auth login`
>
> Then re-run `/devflow-setup`.

### gh not authenticated

> "GitHub CLI installed but not authenticated. Run:"
> ```bash
> gh auth login
> ```
> Then re-run `/devflow-setup`.

### User wants to skip

Set `ISSUES_BACKEND = "none"`, `ISSUES_ENABLED = false`. Return to SKILL.md.

---

## Configuration Values

| Key | Value |
|-----|-------|
| `backend` | `github` |
| Notes | Uses current repo context via gh CLI — no extra config needed |

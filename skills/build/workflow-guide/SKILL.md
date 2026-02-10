---
name: devflow:build:workflow-guide
description: DevFlow workflow overview - discover commands and understand how they connect. Use this to learn about the DevFlow SDLC workflow.
argument-hint: ""
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - Glob
  - Read
---

# DevFlow Workflow Guide

A streamlined development workflow broken into focused phases with human-in-the-loop decision points.

**Multi-Backend Support:** DevFlow works with Jira or GitLab Issues, Confluence or Google Drive, and GitHub PRs or GitLab MRs.

---

## Step 1: Discover Available Commands

Scan the build directory to find all available commands.

```
[Use Glob to find all .md files in .claude/commands/devflow/build/]
[Exclude: workflow-guide.md (this file), reference/ subdirectory]
[For each file, read first 10 lines to extract frontmatter: description, argument-hint]
```

---

## Step 2: Present Workflow Overview

The DevFlow commands follow this progression:

```
fetch-issue → plan-issue → implement-issue → security-review → complete-issue → post-merge
    ↓            ↓             ↓                ↓                 ↓              ↓
 Fetch &     Branch +       Execute        Security          PR/MR +       Cleanup
 Analyze    Plan Mode        Plan            Scan            Close Issue    & Sync
                                          (Recommended)
```

**Core workflow phases:**
1. **Fetch** - Get issue, analyze feasibility
2. **Plan** - Enter Plan Mode, save approved plan
3. **Implement** - Execute plan with validation
4. **Review** - Security scan (recommended)
5. **Complete** - Create PR/MR, update issue status
6. **Cleanup** - Sync and prepare for next issue

**Supported Backends:**

| Component | Options |
|-----------|---------|
| Issues | Jira, GitLab Issues |
| Documentation | Confluence, Google Drive, RAG Memory |
| VCS | GitHub (PRs), GitLab (MRs) |

Run `/devflow-setup` to configure your backends.

---

## Step 3: List Commands with Descriptions

Present each discovered command in this format:

### `/devflow:build:[command-name]` [argument-hint]

**Purpose:** [description from frontmatter]

**Position in workflow:** [Based on command name, indicate where it fits]
- fetch-issue: Start of workflow
- plan-issue: After fetch, before implementation
- implement-issue: After plan approval
- security-review: After implementation (recommended)
- complete-issue: After security review or implementation
- post-merge: After PR/MR merged
- create-issue: Standalone - create new issues

**Next step:** [Indicate what typically comes next]

---

## Step 4: Present Supporting Information

### Key Design Principles

**Generic & Pattern-Driven**
- Commands work across project types (Python, JavaScript, Go, etc.)
- Discover project-specific patterns instead of prescribing
- Adapt validation strategy to work type

**Backend-Agnostic**
- Same workflow for Jira or GitLab Issues
- Same workflow for GitHub PRs or GitLab MRs
- Configuration determines which APIs to call

**Type-Aware Planning**
- Features: Components, integration, testing
- Bugs: Reproduction, root cause, regression tests
- Infrastructure: Validation, impact assessment
- Documentation: Accuracy, examples, links

**Human-in-the-Loop**
- Decision boundaries at critical points
- No auto-proceed past approval gates
- User controls workflow progression

---

### Decision Points

**After Fetch:**
- ✅ Not implemented → Continue to planning
- 🔄 Partially implemented → Review and continue
- ❌ Fully implemented → Close issue
- ⚠️ Conflicts → Discuss with team

**After Planning:**
- ✅ Approve → Proceed to implement
- 📝 Revise → Request changes, review again
- ❌ Reject → Discuss alternative

**After Implementation:**
- ✅ Validated → Run security review (recommended)
- ❌ Failed validation → Fix and re-validate
- 🔄 Major deviation → Auto re-plan with approval

**After Security Review:**
- ✅ No issues → Continue to complete
- ⚠️ Issues found → Fix vulnerabilities, re-run
- ⏭️ Can skip if low-risk (docs only, etc.)

**After Complete:**
- Wait for PR/MR review and merge
- Address feedback if needed
- Run post-merge after merge completes

---

### Quick Start Example

**With Jira + GitHub (default):**
```bash
# 1. Fetch issue and analyze
/devflow:build:fetch-issue ACT-123

# 2. Create branch and plan (after feasibility check)
/devflow:build:plan-issue ACT-123

# 3. Execute plan (after plan approval)
/devflow:build:implement-issue ACT-123

# 4. Security review (recommended)
/devflow:build:security-review ACT-123

# 5. Finalize (create PR, update JIRA)
/devflow:build:complete-issue ACT-123

# 6. Cleanup (after PR merged)
/devflow:build:post-merge
```

**With GitLab Issues + GitLab MRs:**
```bash
# Same commands, different backend
/devflow:build:fetch-issue 42

/devflow:build:plan-issue 42

/devflow:build:implement-issue 42

/devflow:build:security-review 42

/devflow:build:complete-issue 42

/devflow:build:post-merge
```

---

### Configuration

**First-time setup:**
```bash
/devflow-setup
```

This wizard will:
1. Detect available MCP servers
2. Let you choose your backends
3. Save configuration for all commands

**View/change config:**
- Global: `~/.claude/devflow-config.md`
- Project: `.claude/devflow-config.md` (overrides global)

---

### Tips

- Each command preserves context for the next step
- Commands discover patterns - don't fight them
- Git branch naming adapts to issue type (feature/bugfix/task)
- Incremental commits keep changes trackable
- Documentation updates are mandatory, not optional
- Test pattern compliance is enforced, not suggested

---

## Reference Documents

The `references/` subdirectory contains example issues:
- `FEATURE-EXAMPLE.md` - Example Feature/Executable Spec issue
- `BUG-EXAMPLE.md` - Example Bug issue
- `REFERENCE.md` - Issue standards reference

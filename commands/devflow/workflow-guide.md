---
description: DevFlow workflow overview - discover commands and understand how they connect
argument-hint: ""
allowed-tools: ["Glob", "Read"]
---

# DevFlow Workflow Guide

A streamlined JIRA development workflow broken into focused phases with human-in-the-loop decision points.

---

## Step 1: Discover Available Commands

Scan the devflow directory to find all available commands.

```
[Use Glob to find all .md files in .claude/commands/devflow/]
[Exclude: workflow-guide.md (this file), reference/ subdirectory]
[For each file, read first 10 lines to extract frontmatter: description, argument-hint]
```

---

## Step 2: Present Workflow Overview

The devflow commands follow this progression:

```
fetch-issue → plan-work → implement-plan → security-review → complete-issue → post-merge
    ↓            ↓             ↓                ↓                 ↓              ↓
 Fetch &     Branch +       Execute        Security          PR + JIRA      Cleanup
 Analyze    Plan Mode        Plan            Scan              Done          & Sync
                                          (Recommended)
```

**Core workflow phases:**
1. **Fetch** - Get issue, analyze feasibility
2. **Plan** - Enter Plan Mode, save approved plan
3. **Implement** - Execute plan with validation
4. **Review** - Security scan (recommended)
5. **Complete** - Create PR, update JIRA
6. **Cleanup** - Sync and prepare for next issue

---

## Step 3: List Commands with Descriptions

Present each discovered command in this format:

### `/devflow:[command-name]` [argument-hint]

**Purpose:** [description from frontmatter]

**Position in workflow:** [Based on command name, indicate where it fits]
- fetch-issue: Start of workflow
- plan-work: After fetch, before implementation
- implement-plan: After plan approval
- security-review: After implementation (recommended)
- complete-issue: After security review or implementation
- post-merge: After PR merged
- create-issue: Standalone - create new JIRA issues

**Next step:** [Indicate what typically comes next]

---

## Step 4: Present Supporting Information

### Key Design Principles

**Generic & Pattern-Driven**
- Commands work across project types (Python, JavaScript, Go, etc.)
- Discover project-specific patterns instead of prescribing
- Adapt validation strategy to work type

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
- Wait for PR review and merge
- Address feedback if needed
- Run post-merge after merge completes

---

### Quick Start Example

```bash
# 1. Fetch issue and analyze
/devflow:fetch-issue ACT-123

# 2. Create branch and plan (after feasibility check)
/devflow:plan-work ACT-123

# 3. Execute plan (after plan approval)
/devflow:implement-plan

# 4. Security review (recommended)
/devflow:security-review ACT-123

# 5. Finalize (create PR, update JIRA)
/devflow:complete-issue ACT-123

# 6. Cleanup (after PR merged)
/devflow:post-merge
```

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

The `reference/` subdirectory contains example issues:
- `FEATURE-EXAMPLE.md` - Example Executable Spec issue
- `BUG-EXAMPLE.md` - Example Bug issue
- `REFERENCE.md` - JIRA issue standards reference

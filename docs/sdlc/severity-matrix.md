# Bug Severity and Priority Matrix

A practical framework for classifying bugs and deciding how urgently to fix them.

---

## Severity Levels

Severity describes **how bad the bug is**. It's an objective assessment of impact.

| Level | Label | Description | Examples |
|-------|-------|-------------|----------|
| **Critical** | `Critical` | System is down, data loss, or security vulnerability | App won't load, database corruption, XSS vulnerability, payments broken |
| **High** | `High` | Major feature is broken, no workaround | Search returns no results, login fails, form can't submit |
| **Medium** | `Medium` | Feature works but with significant issues | Filter resets on page change, slow load times, layout broken on mobile |
| **Low** | `Low` | Cosmetic or minor inconvenience | Typo in UI, slight misalignment, tooltip shows wrong text |

---

## Priority Mapping

Priority describes **how soon to fix it**. It combines severity with business context.

| Severity | Default Priority | Rationale |
|----------|-----------------|-----------|
| **Critical** | `priority:high` | Fix immediately — drop what you're doing |
| **High** | `priority:high` | Fix before starting new features |
| **Medium** | *(no label)* | Fix in normal workflow order |
| **Low** | `priority:low` | Fix when convenient, or batch with related work |

> **Why not 4 priority levels?** For a solo dev or small team, the decision is really just "fix now" vs. "fix later" vs. "fix whenever." Two labels plus "no label = normal" covers this cleanly.

---

## Decision Guide

### When to override the default mapping

Severity and priority usually align, but not always:

| Scenario | Severity | Priority | Why |
|----------|----------|----------|-----|
| Typo on the landing page | Low | `priority:high` | First impression matters |
| Broken feature nobody uses | High | `priority:low` | No users affected |
| Security flaw in staging | Critical | *(normal)* | Not in production yet |
| Cosmetic bug right before launch | Low | `priority:high` | Timing matters |

The PO decides priority. Severity is a fact; priority is a judgment call.

---

## Response Times

Guidelines, not SLAs. Adjust for your project's context.

| Priority | Response | Meaning |
|----------|----------|---------|
| `priority:high` | Same session | Stop current work, fix this first |
| *(normal)* | Next available slot | Pick it up when the current task is done |
| `priority:low` | When convenient | Batch with related work or tackle during downtime |

---

## Using Severity in Bug Reports

The bug issue template (`.github/ISSUE_TEMPLATE/bug.yml`) includes a Severity dropdown with these four levels. When filing a bug:

1. **Select the severity** based on the descriptions above
2. **The dev or PO adds a priority label** if it differs from the default mapping
3. **No priority label** means normal priority (fix in backlog order)

---

## Triage Checklist

When a new bug comes in:

1. **Is it really a bug?** Or is it working as designed? Check the spec.
2. **What's the severity?** Use the table above. Be honest — not everything is Critical.
3. **Does priority match severity?** If not, add a priority label and note why.
4. **Is there a workaround?** Document it in the issue for users in the meantime.
5. **Does it block other work?** If yes, set it as a blocker on the board.

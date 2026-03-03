# Definition of Done

A change is not complete until every applicable item on its checklist is satisfied. These checklists are the exit criteria for moving an issue from **In Progress** to **Verify**.

---

## By Issue Type

### Feature

A new feature or enhancement to existing functionality.

- [ ] **Code complete** — Feature works as described in acceptance criteria
- [ ] **Follows existing patterns** — Code matches project conventions and style
- [ ] **No regressions** — Existing features still work correctly
- [ ] **Spec updated** — Project specification reflects the new behavior
- [ ] **CLAUDE.md updated** — File structure, patterns, or architecture changes documented
- [ ] **README.md updated** — If the feature is user-facing or changes setup
- [ ] **Commit references ticket** — All commits include `#XX`
- [ ] **Ready for human verification** — Card moved to Verify column

### Bug Fix

Something was broken and now it's fixed.

- [ ] **Bug fixed** — The reported behavior no longer occurs
- [ ] **Root cause understood** — You know why it happened, not just how to suppress it
- [ ] **No regressions** — The fix doesn't break anything else
- [ ] **Spec updated** — If the fix changes documented behavior
- [ ] **Commit references ticket** — All commits include `#XX`
- [ ] **Ready for human verification** — Card moved to Verify column

### Documentation

A change to documentation files only (no code changes).

- [ ] **Content accurate** — Documentation matches current code behavior
- [ ] **Consistent across docs** — Spec, CLAUDE.md, and README.md agree with each other
- [ ] **No broken links** — All references and cross-links work
- [ ] **Formatting correct** — Markdown renders properly
- [ ] **Commit references ticket** — All commits include `#XX`
- [ ] **Ready for human review** — Card moved to Verify column

### Task

Refactors, dependency updates, tooling, or infrastructure changes.

- [ ] **Change implemented** — The refactor, update, or config change is in place
- [ ] **No regressions** — Nothing is broken by the change
- [ ] **No behavior changes** — Unless explicitly intended (in which case, treat as a feature)
- [ ] **Documentation updated** — If the change affects project structure or setup
- [ ] **Commit references ticket** — All commits include `#XX`
- [ ] **Ready for human verification** — Card moved to Verify column

### Spike

Research, investigation, or proof-of-concept to answer a question.

- [ ] **Question answered** — Or explicitly marked unanswerable with current information
- [ ] **Findings documented** — In issue comments or a linked document
- [ ] **Recommendation provided** — With tradeoffs clearly stated
- [ ] **Follow-up tickets created** — If the spike produced actionable next steps
- [ ] **Ready for human review** — Card moved to Verify column

---

## Universal Rules

These apply to every issue type:

1. **Documentation is not optional.** If a change affects behavior, the spec must be updated in the same PR. A change without updated documentation is incomplete.

2. **Human verification is required.** The person or AI that wrote the code cannot mark it as Done. The Verify column exists for the human to confirm the work.

3. **Ticket references are required.** Every commit must include the issue number (`#XX: description`). This creates traceability from code back to the decision that authorized it.

4. **"It works on my machine" is not done.** Verify across the target environments (mobile/desktop, different browsers, etc.) as applicable.

---

## How to Use These Checklists

### In issue templates
The issue templates (`.github/ISSUE_TEMPLATE/`) include a "Definition of Done" field pre-populated with the relevant checklist. Customize it per-issue as needed.

### In pull requests
The PR template (`.github/PULL_REQUEST_TEMPLATE.md`) includes documentation and testing checklists. Review these before requesting verification.

### As a reviewer
When you're wearing the QA hat and verifying work in the Verify column, walk through the applicable checklist. If any item isn't satisfied, send it back to In Progress with a comment explaining what's missing.

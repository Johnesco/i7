# Commit and Branch Conventions

Consistent naming for commits, pull requests, and branches.

---

## Commit Messages

### Format

```
#XX: Short description of what changed
```

- `#XX` is the GitHub Issue number
- Description is imperative mood ("Add feature", not "Added feature")
- Keep the first line under 72 characters
- No period at the end

### Examples

```
#12: Add user avatar upload component
#7: Fix search not clearing on view switch
#34: Update functional spec with date range section
#5: Refactor venue service to use async/await
```

### Multi-line commits

For larger changes, add a blank line and body:

```
#12: Add user avatar upload component

- New AvatarUpload component with drag-and-drop
- Image validation (max 2MB, jpg/png only)
- Preview thumbnail before save
```

### Commits without tickets

Some commits don't need a ticket (initial setup, merge commits, etc.). For these, use a descriptive message without a ticket reference:

```
Initial project setup
Merge branch 'feature/avatar' into main
```

### AI co-authorship

When an AI assistant writes or significantly contributes to a commit, include a co-author trailer:

```
#12: Add user avatar upload component

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## Pull Requests

### Title format

```
#XX: Short description
```

Same as commit messages. Keep under 72 characters.

### Body format

```markdown
## Summary
Brief description of what this PR does and why.

## Related Issue
Fixes #XX

## Changes
- Bullet list of what changed

## Documentation Checklist
- [ ] Project spec updated
- [ ] CLAUDE.md updated
- [ ] README.md updated
- [ ] No doc updates needed

## Testing Checklist
- [ ] Manually tested happy path
- [ ] Edge cases verified
- [ ] No regressions
```

> The `.github/PULL_REQUEST_TEMPLATE.md` file provides this format automatically.

### Auto-closing issues

Use `Fixes #XX` in the PR body (not just the title) to auto-close the issue when the PR is merged. GitHub recognizes these keywords:

- `Fixes #XX`
- `Closes #XX`
- `Resolves #XX`

---

## Branch Naming

### Format

```
[type]/[short-description]
```

### Types

| Prefix | Use for |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `task/` | Refactors, tooling, dependencies |
| `spike/` | Research, investigation |

### Examples

```
feature/avatar-upload
fix/search-clear-bug
docs/update-api-spec
task/upgrade-dependencies
spike/auth-provider-comparison
```

### Rules

- Use lowercase and hyphens (no underscores, no camelCase)
- Keep it short but descriptive
- Include the issue number if helpful: `feature/12-avatar-upload`

---

## When to Branch

### Always branch for:
- Features that touch multiple files
- Changes that need review before merging
- Work that might take more than one session

### OK to commit directly to main for:
- Single-file data updates (adding a record)
- Typo fixes
- Documentation-only changes
- Solo projects where you're the only contributor

> This is a guideline, not a rule. Solo projects can commit to main freely. Teams should always branch.

---

## Summary

| Element | Format | Example |
|---------|--------|---------|
| Commit message | `#XX: description` | `#12: Add avatar upload` |
| PR title | `#XX: description` | `#12: Add avatar upload` |
| PR body keyword | `Fixes #XX` | `Fixes #12` |
| Branch name | `type/description` | `feature/avatar-upload` |

# Label Taxonomy

A consistent labeling system for GitHub Issues. Labels are grouped into four categories: **Type**, **Area**, **Priority**, and **Resolution**.

---

## Label Categories

### Type Labels

Every issue gets exactly **one** type label.

| Label | Color | Description |
|-------|-------|-------------|
| `feature` | `#1d76db` | New functionality or enhancement |
| `bug` | `#d73a4a` | Something isn't working correctly |
| `docs` | `#0075ca` | Documentation-only changes |
| `task` | `#e4e669` | Refactors, dependencies, tooling, infrastructure |
| `spike` | `#c29cf0` | Research, investigation, or proof-of-concept |

### Area Labels

Issues get **one or more** area labels to indicate which part of the codebase is affected.

| Label | Color | Description |
|-------|-------|-------------|
| `area:frontend` | `#c5def5` | UI components, views, styles |
| `area:backend` | `#bfdadc` | Server, API, database |
| `area:data` | `#d4c5f9` | Data model, schema, migrations |
| `area:docs` | `#fef2c0` | Documentation files |
| `area:infra` | `#f9d0c4` | CI/CD, deployment, tooling |
| `area:testing` | `#e6e6e6` | Tests, test infrastructure |
| `area:design` | `#fbca04` | UI/UX design, styling |

> **Customize these for your project.** Not every project needs all area labels. A frontend-only project might just use `area:components`, `area:views`, `area:styles`. A backend API might use `area:routes`, `area:models`, `area:auth`.

### Priority Labels

Issues get **at most one** priority label. Most issues don't need one — use priority labels only to call out items that are unusually high or low priority.

| Label | Color | Description |
|-------|-------|-------------|
| `priority:high` | `#b60205` | Must be addressed soon |
| `priority:low` | `#c2e0c6` | Nice to have, no urgency |

> **Why only two?** With a solo dev or small team, a simple high/low split is enough. Everything without a priority label is "normal" priority. See [`severity-matrix.md`](severity-matrix.md) for how bug severity maps to these labels.

### Resolution Labels

Applied when closing an issue that was **not completed normally**. Issues closed without a resolution label are implicitly "Completed."

| Label | Color | Description |
|-------|-------|-------------|
| `resolution:wontfix` | `#d1d5db` | Deliberately declined by PO |
| `resolution:duplicate` | `#d1d5db` | Already covered by another issue |
| `resolution:cannot-reproduce` | `#d1d5db` | Bug can't be replicated |
| `resolution:by-design` | `#d1d5db` | Reported behavior is intentional, not a bug |
| `resolution:stale` | `#d1d5db` | Issue went inactive, no longer relevant |
| `resolution:superseded` | `#d1d5db` | Replaced by a different ticket or approach |

> **Convention:** No resolution label = completed. Only add a resolution label when closing an issue without doing the work. Use GitHub's "Close as not planned" option alongside the resolution label.

> **Always comment before closing:** When applying any resolution label, add a comment explaining why. For `resolution:duplicate` and `resolution:superseded`, link to the related issue.

---

## Setup Commands

### Using the `gh` CLI

Run these commands to create all labels in your repository:

```bash
# Type labels
gh label create "feature" --color "1d76db" --description "New functionality or enhancement"
gh label create "bug" --color "d73a4a" --description "Something isn't working correctly"
gh label create "docs" --color "0075ca" --description "Documentation-only changes"
gh label create "task" --color "e4e669" --description "Refactors, dependencies, tooling, infrastructure"
gh label create "spike" --color "c29cf0" --description "Research, investigation, or proof-of-concept"

# Area labels
gh label create "area:frontend" --color "c5def5" --description "UI components, views, styles"
gh label create "area:backend" --color "bfdadc" --description "Server, API, database"
gh label create "area:data" --color "d4c5f9" --description "Data model, schema, migrations"
gh label create "area:docs" --color "fef2c0" --description "Documentation files"
gh label create "area:infra" --color "f9d0c4" --description "CI/CD, deployment, tooling"
gh label create "area:testing" --color "e6e6e6" --description "Tests, test infrastructure"
gh label create "area:design" --color "fbca04" --description "UI/UX design, styling"

# Priority labels
gh label create "priority:high" --color "b60205" --description "Must be addressed soon"
gh label create "priority:low" --color "c2e0c6" --description "Nice to have, no urgency"

# Resolution labels
gh label create "resolution:wontfix" --color "d1d5db" --description "Deliberately declined by PO"
gh label create "resolution:duplicate" --color "d1d5db" --description "Already covered by another issue"
gh label create "resolution:cannot-reproduce" --color "d1d5db" --description "Bug can't be replicated"
gh label create "resolution:by-design" --color "d1d5db" --description "Reported behavior is intentional, not a bug"
gh label create "resolution:stale" --color "d1d5db" --description "Issue went inactive, no longer relevant"
gh label create "resolution:superseded" --color "d1d5db" --description "Replaced by a different ticket or approach"
```

> You can also run `scripts/setup-labels.sh` to execute all of these at once.

### Removing GitHub's default labels

New repos come with default labels (`enhancement`, `good first issue`, `help wanted`, etc.) that overlap with this system. Remove them if you prefer a clean slate:

```bash
gh label delete "enhancement" --yes
gh label delete "good first issue" --yes
gh label delete "help wanted" --yes
gh label delete "invalid" --yes
gh label delete "question" --yes
gh label delete "wontfix" --yes
gh label delete "duplicate" --yes
gh label delete "documentation" --yes
```

> Keep the default `bug` label if its color matches — or delete it and recreate with the color above.

---

## Usage Guidelines

### Assigning labels on issue creation

```bash
gh issue create \
  --title "Add search bar to header" \
  --label "feature,area:frontend" \
  --milestone "Search & Filtering"
```

Multiple labels are comma-separated. Always include at least the type label.

### Closing with a resolution

```bash
# Close as not planned with a resolution label
gh issue edit 42 --add-label "resolution:wontfix"
gh issue close 42 --reason "not planned"

# Close a duplicate (always link the original first)
gh issue comment 42 --body "Duplicate of #15"
gh issue edit 42 --add-label "resolution:duplicate"
gh issue close 42 --reason "not planned"
```

### Querying by label

```bash
# All open bugs
gh issue list --label "bug"

# High-priority frontend features
gh issue list --label "feature,area:frontend,priority:high"

# All docs-related issues (any type)
gh issue list --label "area:docs"

# All spikes
gh issue list --label "spike"

# All issues closed as won't fix
gh issue list --state closed --label "resolution:wontfix"

# All non-completed closures
gh issue list --state closed --label "resolution:wontfix,resolution:duplicate,resolution:stale"
```

---

## Customizing for Your Project

### Adding area labels

If your project has distinct areas not covered above:

```bash
gh label create "area:auth" --color "d4c5f9" --description "Authentication and authorization"
gh label create "area:search" --color "c5def5" --description "Search and filtering"
```

### Recommended approach

1. Start with Type + Priority + Resolution labels (13 labels)
2. Add Area labels as you create your first few issues
3. Don't create area labels speculatively — wait until you have an issue that needs one
4. Keep the total under 30 labels to stay manageable

# GitHub Projects Board Setup

Step-by-step guide to creating the 5-column kanban board that drives this workflow.

---

## Prerequisites

- A GitHub repository (public or private)
- The [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Repository owner or admin permissions

---

## Step 1: Create the Project

1. Go to your GitHub profile or organization
2. Click **Projects** tab → **New project**
3. Select **Board** layout
4. Name it (e.g., your project name)
5. Click **Create project**

Or via CLI:

```bash
gh project create --owner [YOUR_USERNAME] --title "[Project Name]"
```

> Note the project number that's returned — you'll need it for `gh project item-add`.

---

## Step 2: Configure Columns

The default board has 3 columns (Todo, In Progress, Done). You need 5:

### Rename existing columns
1. Click the **Todo** column header → Rename to **Backlog**
2. Keep **In Progress** as-is
3. Keep **Done** as-is

### Add new columns
Add these columns between the existing ones (click **+** to add):

4. **Ready** — place after Backlog
5. **Verify** — place after In Progress

### Final column order

```
Backlog → Ready → In Progress → Verify → Done
```

---

## Step 3: Set Up Automations

GitHub Projects has built-in workflow automations. Enable these:

### Auto-set status when items are added
1. In the project, click **⋯** (menu) → **Workflows**
2. Find **Item added to project** → Enable it
3. Set: When an item is added → Set status to **Backlog**

### Auto-close items when done
1. Find **Item closed** → Enable it
2. Set: When an item is closed → Set status to **Done**

### Auto-reopen items
1. Find **Item reopened** → Enable it
2. Set: When an item is reopened → Set status to **In Progress**

### Pull request merged
1. Find **Pull request merged** → Enable it
2. Set: When a PR is merged → Set status to **Done**

### Summary of automations

| Trigger | Sets Status To |
|---------|---------------|
| Item added to project | **Backlog** |
| Item closed | **Done** |
| Item reopened | **In Progress** |
| Pull request merged | **Done** |

### Manual transitions

These transitions are **not** automated and must be set by the developer or AI during the workflow:

| Transition | When |
|------------|------|
| Backlog → Ready | Refinement checklist complete, acceptance criteria finalized |
| Ready → In Progress | Coding begins |
| In Progress → Verify | Code is complete, awaiting human testing |

---

## Step 4: Link Issues to the Board

This is the most important operational step.

> **`gh issue create` does NOT automatically add issues to the project board.**

After every `gh issue create`, you must also run:

```bash
gh project item-add [PROJECT_NUMBER] --owner [YOUR_USERNAME] --url [ISSUE_URL]
```

### Example workflow

```bash
# Create the issue
ISSUE_URL=$(gh issue create \
  --title "Add user authentication" \
  --label "feature" \
  --milestone "User Accounts" \
  --body "Users should be able to log in..." \
  | tail -1)

# Add it to the project board
gh project item-add 1 --owner myusername --url "$ISSUE_URL"
```

### Why this matters

If you skip the `item-add` step:
- The issue exists but is invisible on the board
- Board automations (like auto-moving to Done when closed) won't fire
- The issue effectively drops out of the workflow

This is a known GitHub limitation, not a bug. Build it into your muscle memory.

---

## Step 5: Find Your Project IDs (Advanced)

If you're scripting board operations, you'll need the project's internal IDs.

### Get the project ID

```bash
gh project list --owner [YOUR_USERNAME]
```

This shows the project number. To get the full node ID (needed for GraphQL):

```bash
gh project view [PROJECT_NUMBER] --owner [YOUR_USERNAME] --format json | jq '.id'
```

### Get field and option IDs

To programmatically move items between columns, you need the Status field ID and option IDs:

```bash
gh project field-list [PROJECT_NUMBER] --owner [YOUR_USERNAME] --format json
```

Look for the "Status" field and note the field ID and each option's ID.

### Move an item programmatically

```bash
gh project item-edit \
  --project-id [PROJECT_ID] \
  --id [ITEM_ID] \
  --field-id [STATUS_FIELD_ID] \
  --single-select-option-id [OPTION_ID]
```

> Store these IDs in your project's CLAUDE.md or memory files so your AI assistant can move cards without looking them up each time.

---

## Checklist

After setup, verify:

- [ ] 5 columns in correct order: Backlog → Ready → In Progress → Verify → Done
- [ ] "Item added" automation sets status to Backlog
- [ ] "Item closed" automation sets status to Done
- [ ] "Item reopened" automation sets status to In Progress
- [ ] "PR merged" automation sets status to Done
- [ ] Test: create an issue, add it to the board, confirm it lands in Backlog
- [ ] Test: close the issue, confirm it moves to Done

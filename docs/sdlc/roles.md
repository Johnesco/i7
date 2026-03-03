# Roles and AI Collaboration Model

This document defines the roles in the development workflow and how they map to a solo developer working with an AI coding assistant.

---

## Role Definitions

### PO — Product Owner

**Typical owner:** Human (always)

**Responsibilities:**
- Decide what gets built and in what order
- Prioritize the backlog
- Accept or reject completed work
- Resolve discrepancies between code and documentation (final say)

**Board columns owned:** Backlog, Done

**When wearing this hat, you might say:**
- "Let's prioritize the backlog for this week."
- "This is accepted — close the issue."
- "The spec is correct, update the code to match."

---

### BA — Business Analyst

**Typical owner:** Human or AI

**Responsibilities:**
- Scope features and write acceptance criteria
- Review documentation for affected areas before changes
- Flag discrepancies between code and docs
- Refine tickets with context, affected files, and doc impact
- Draft issue descriptions in user-story format

**Board columns owned:** Backlog (refinement), Ready

**When wearing this hat, you might say:**
- "Help me scope this feature — what files would be affected?"
- "Review the spec for Section 7 before we start."
- "The acceptance criteria need to include error states."

**AI capabilities in this role:**
- Can draft tickets and acceptance criteria
- Can identify affected documentation sections
- Can spot discrepancies between code and docs
- Cannot make final decisions on scope (that's PO)

---

### Dev — Developer

**Typical owner:** AI (primary) or Human

**Responsibilities:**
- Write code that implements the ticket requirements
- Reference ticket numbers in commits (`#XX: description`)
- Follow existing code patterns and conventions
- Read files before editing them
- Keep changes focused on ticket scope

**Board columns owned:** In Progress

**When wearing this hat, you might say:**
- "Implement ticket #12."
- "Write the code for the avatar upload feature."

**AI capabilities in this role:**
- Writes code following project conventions
- Identifies and follows existing patterns
- Keeps changes scoped to the ticket
- Commits with proper references

---

### Documenter

**Typical owner:** AI (bundled with Dev role)

**Responsibilities:**
- Update the project spec when features change
- Update CLAUDE.md when structure or patterns change
- Update README.md when public-facing features change
- Ensure all documentation stays consistent after changes

**Board columns owned:** In Progress (same as Dev)

In practice, the Dev and Documenter roles are performed by the same person/AI in the same work session. Code and documentation are updated together, not as separate tasks.

**AI capabilities in this role:**
- Updates documentation consistently and thoroughly
- Catches sections that need updating across multiple files
- Maintains consistent formatting and conventions
- Treats documentation as part of the deliverable, not an afterthought

---

### QA — Quality Assurance

**Typical owner:** Human (always)

**Responsibilities:**
- Verify that completed work matches acceptance criteria
- Test features in the actual application
- Confirm documentation accurately describes behavior
- Identify edge cases and regressions
- Accept or send back for rework

**Board columns owned:** Verify

> **The most important rule in this entire process:**
> **Claude cannot QA its own work.**
>
> The Verify column is always human-owned. The person or AI that wrote the code is not qualified to verify it — they have blind spots about their own output. Human verification is what closes the loop and makes the process trustworthy.

**When wearing this hat, you might say:**
- "I'm going to verify ticket #12 now."
- "The feature works but the edge case with empty input isn't handled."
- "Sending this back — the spec says X but the code does Y."

---

## Role Summary Table

| Role | Typical Owner | Board Columns | Can AI Do It? |
|------|---------------|---------------|---------------|
| **PO** | Human | Backlog, Done | No — requires human judgment |
| **BA** | Human or AI | Backlog (refinement), Ready | Yes — with human oversight |
| **Dev** | AI or Human | In Progress | Yes — primary AI role |
| **Documenter** | AI (with Dev) | In Progress | Yes — bundled with Dev |
| **QA** | **Human** | **Verify** | **No — cannot self-verify** |

---

## Hat-Switch Protocol

When working with an AI assistant, explicitly state which role you're operating in. This prevents the AI from guessing your intent and keeps the interaction predictable.

### How to switch hats

Use a clear verbal signal at the start of a message:

```
"PO hat — let's review what's in the backlog and pick the next 3 items."
```

```
"BA mode — help me scope the search feature. What does the spec say about it today?"
```

```
"Dev time — implement ticket #15. Follow the patterns in ComponentX."
```

```
"QA check — I'm testing ticket #15. The filter doesn't clear when I switch views."
```

### Why this matters

Without explicit role signals, the AI might:
- Start coding when you wanted to discuss scope (jumped from BA to Dev)
- Update documentation when you wanted to verify first (jumped from QA to Documenter)
- Make priority decisions that should be yours (assumed PO role)

With role signals:
- The AI knows what kind of help you need
- Responses match the expected level of detail
- Workflow steps happen in the right order
- The human stays in control of decisions

### Multiple hats in one session

It's normal to switch roles multiple times in a single session:

```
"BA hat — let's scope ticket #20."
[Discussion about requirements]

"OK, the acceptance criteria look good. Dev mode — implement it."
[AI writes code]

"Documenter check — did you update the spec?"
[AI confirms or updates docs]

"I'll put on the QA hat and test this myself. Move the card to Verify."
```

---

## Solo Dev Without AI

This role model works even without an AI assistant. As a solo developer, you wear all the hats yourself, but the discipline of switching between them remains valuable:

- **PO hat:** Decide what to build next (don't just grab the first thing that looks interesting)
- **BA hat:** Scope it before coding (write the acceptance criteria, check the docs)
- **Dev hat:** Build it (reference the ticket, follow conventions)
- **Documenter hat:** Update the docs (don't skip this — future-you is your teammate)
- **QA hat:** Test it with fresh eyes (step away, come back, test like a user)

The roles exist to prevent the most common solo-dev failure mode: jumping straight from idea to code and never documenting, testing, or verifying.

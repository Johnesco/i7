# Cloak of Darkness (Rez)

The standard IF benchmark game implemented in Rez — an open-source choice-based IF language/compiler/runtime.

For build, test, and publish workflows, see `C:\code\ifhub\reference\project-guide.md`.

## Game Overview

- **Engine**: Rez (choice-based, compiles to static HTML)
- **Max score**: 2 points
- **Rooms**: Foyer, Cloakroom, Bar
- **Core mechanic**: Hang cloak to illuminate bar, read undisturbed message to win

## Scoring

| Action | Points |
|--------|--------|
| Hang cloak on hook | +1 |
| Read message (< 2 disturbances) | +1 (win) |
| Read message (>= 2 disturbances) | 0 (lose) |

## Build

```bash
# Build + import from Rez workspace:
python tools/compile_rez.py cloak-rez

# Register + publish:
python tools/register_game.py --name cloak-rez --title "Cloak of Darkness (Rez)" --engine rez --tags "cloak,demo"
python tools/publish.py cloak-rez
```

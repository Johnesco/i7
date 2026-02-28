# IF Hub

Central hub for Inform 7 authoring, compilation, testing, and web deployment. All Inform 7 projects under `C:\code\` reference this location for shared tooling, reference docs, and the Parchment web player.

## Quick Start

```bash
# Create a new project
bash tools/new-project.sh "My Game" mygame

# Edit the source
# (edit projects/mygame/story.ni)

# Compile and set up web player
bash tools/compile.sh mygame

# Play locally
python -m http.server 8000 --directory projects/mygame/web
# Open http://localhost:8000/play.html

# Run tests (via WSL)
cd projects/mygame && wsl -e bash tests/run-tests.sh

# Publish to GitHub Pages
bash tools/publish.sh mygame
```

## Directory Structure

```
ifhub/
├── README.md              ← You are here
├── CLAUDE.md              ← AI assistant instructions and full conventions
├── reference/             ← Inform 7 language reference docs
│   ├── syntax-guide.md
│   ├── text-formatting.md
│   ├── world-model.md
│   ├── understanding.md
│   ├── lists.md
│   ├── extensions.md
│   ├── descriptions-adaptive-text.md
│   ├── rulebooks.md
│   └── activities-phrases.md
├── tools/                 ← Shared scripts (see tools/README.md)
│   ├── compile.sh
│   ├── new-project.sh
│   ├── publish.sh
│   ├── build-site.sh
│   ├── snapshot.sh
│   ├── regtest.py
│   ├── testing/           ← Generic testing framework
│   └── web/               ← Parchment web player setup
├── projects/              ← Game projects
│   ├── dracula/
│   ├── feverdream/
│   ├── sample/
│   └── zork1/
└── ifhub/                 ← IF Hub multi-game web player
```

## Projects

| Project | Description | Web |
|---------|-------------|-----|
| **zork1** | Zork I: Inform 7 Edition (ZIL-to-I7 translation) | [Play](https://johnesco.github.io/zork1/) |
| **dracula** | Dracula's Castle | [Play](https://johnesco.github.io/dracula/) |
| **feverdream** | Fever Dream | — |
| **sample** | Sample practice game (local-only) | — |

Each project has its own `story.ni` source file, test suite, and optional web player. See each project's `CLAUDE.md` or `README.md` for details.

## Tools Overview

All scripts live in `tools/`. See [`tools/README.md`](tools/README.md) for full documentation.

| Script | Purpose |
|--------|---------|
| `new-project.sh` | Scaffold a new Inform 7 project with build, test, and deploy infrastructure |
| `compile.sh` | Compile a project (I7 → I6 → Glulx) and update its web player |
| `publish.sh` | Publish a project to GitHub Pages (creates repo on first run) |
| `build-site.sh` | Assemble `_site/` from `web/` + version snapshots for deployment |
| `snapshot.sh` | Freeze current source into a numbered version snapshot |
| `regtest.py` | Shared RegTest runner (by Andrew Plotkin) for regression testing |

### Testing Framework (`tools/testing/`)

| Script | Purpose |
|--------|---------|
| `run-walkthrough.sh` | Run a walkthrough with optional RNG seeding and diagnostics |
| `find-seeds.sh` | Sweep RNG seeds to find deterministic golden seeds |
| `run-tests.sh` | Run RegTest regression tests for a project |

### Web Player (`tools/web/`)

| Script / File | Purpose |
|----------------|---------|
| `setup-web.sh` | Bootstrap a Parchment web player for any project |
| `play-template.html` | HTML template for player pages |
| `parchment/` | Shared Parchment library files (7 required files) |

## IF Hub Web Player (`ifhub/`)

A standalone static site that serves multiple games through a unified browser interface with source viewer. See [`ifhub/CLAUDE.md`](ifhub/CLAUDE.md) for details.

| Script / File | Purpose |
|----------------|---------|
| `deploy.sh` | Gather game assets from projects into `games/` |
| `games.json` | Game registry (id, title, binary path, sound flag) |
| `app.html` | Player UI with game selector and source viewer |

## Compiler

Inform 7 is installed system-wide. CLI compilation uses `-source` and `-o` flags — no `.inform/` IDE bundles.

```bash
# Compile via compile.sh (recommended)
bash tools/compile.sh <game-name>

# Or manually:
# Step 1: I7 → I6
"/c/Program Files/Inform7IDE/Compilers/inform7.exe" \
    -internal "/c/Program Files/Inform7IDE/Internal" \
    -source /path/to/story.ni -o /path/to/story.i6 -silence

# Step 2: I6 → Glulx
"/c/Program Files/Inform7IDE/Compilers/inform6.exe" -w -G \
    /path/to/story.i6 /path/to/output.ulx
```

## Testing

Tests run in WSL using Glulx/Z-machine interpreters. Each project has a `tests/` directory with thin wrapper scripts that delegate to the generic framework in `tools/testing/`.

**Prerequisites** (WSL):
- **glulxe**: `~/glulxe/glulxe` (Glulx interpreter for Inform 7 games)
- **dfrotz**: `~/frotz-install/usr/games/dfrotz` (Z-machine interpreter for ZIL games)

```bash
# Run regression tests
wsl -e bash tests/run-tests.sh

# Run walkthrough with golden seed
wsl -e bash tests/run-walkthrough.sh

# Find working seeds after code changes
wsl -e bash tests/find-seeds.sh
```

See `tools/README.md` for the full testing framework documentation.

## Reference Docs

The `reference/` directory contains Inform 7 language reference documentation:

- **syntax-guide.md** — Core syntax, kinds, properties, rooms, actions
- **text-formatting.md** — Text substitutions and output formatting
- **world-model.md** — Advanced kinds, properties, rooms/regions/backdrops, relations
- **understanding.md** — Understand command, parser tokens, grammar
- **lists.md** — List operations, sorting, iteration
- **extensions.md** — Extension system: including, authoring, versioning
- **descriptions-adaptive-text.md** — Descriptions, quantifiers, adaptive text
- **rulebooks.md** — Action processing, rules, going, persuasion, senses
- **activities-phrases.md** — Activities, phrase definitions, control flow

# Tools

Shared scripts for compiling, testing, and deploying Inform 7 projects.

## Project Lifecycle Scripts

These are the main scripts you'll use day-to-day. All take a `<game-name>` argument matching a directory under `projects/`.

### `new-project.sh` — Create a New Project

Scaffolds a complete project with source, tests, CI, and documentation.

```bash
bash tools/new-project.sh "Game Title" game-name
```

Creates:
- `story.ni` — Starter Inform 7 source
- `CLAUDE.md` — Project guide
- `.gitignore` — Build output, IDE files
- `.github/workflows/deploy-pages.yml` — GitHub Pages deployment
- `tests/` — Full test suite (project.conf, wrapper scripts, starter regtest, walkthrough)

### `compile.sh` — Compile a Project

Runs the full compilation pipeline and updates the web player.

```bash
bash tools/compile.sh <game-name>
```

Steps:
1. Inform 7 → Inform 6 (via `inform7.exe`)
2. Inform 6 → Glulx (via `inform6.exe`)
3. Clean up intermediate `.i6` file
4. Update web player (copies Parchment libs, base64-encodes `.ulx`)

Output: `projects/<name>/<name>.ulx` and `projects/<name>/web/play.html`

### `publish.sh` — Publish to GitHub Pages

Publishes a project to GitHub Pages. On first run, creates the GitHub repo and enables Pages. On subsequent runs, commits and pushes changes.

```bash
bash tools/publish.sh <game-name>
bash tools/publish.sh <game-name> "commit message"
```

Publishes to: `johnesco.github.io/<game-name>/`

### `build-site.sh` — Assemble Site for Deployment

Assembles a deployable `_site/` directory from `web/` + version snapshots. Used by projects with multiple playable versions (like zork1).

```bash
bash tools/build-site.sh <game-name>
```

Copies `web/*` into `_site/`, then overlays each `versions/vN/` as `_site/vN/`. Serve locally with `python -m http.server 8000 --directory _site`.

### `snapshot.sh` — Freeze a Version Snapshot

Creates or updates a frozen version snapshot in `versions/<version>/`.

```bash
# Create new version (copies from previous version's template)
bash tools/snapshot.sh <game-name> v4

# Update existing version (refreshes source, binary, walkthrough data)
bash tools/snapshot.sh <game-name> v3 --update
```

New version creates:
- `story.ni` — Frozen copy of current source
- `lib/parchment/<name>.ulx.js` — Base64-encoded binary
- Template files (player pages, libs) copied from previous version

Update mode overwrites:
- `story.ni` — Re-synced from project root
- `<name>.ulx.js` — Re-encoded from current binary
- Walkthrough files — Copied from `tests/inform7/` if present

---

## Testing Framework (`testing/`)

A config-driven framework for testing Inform 7 games. Each project defines a `tests/project.conf` with engine paths, score patterns, and diagnostic settings. The framework scripts read this config and do the rest.

### Configuration (`project.conf`)

A bash-sourceable file defining project-specific settings. Key variables:

| Variable | Purpose |
|----------|---------|
| `PROJECT_NAME` | Display name for output |
| `PRIMARY_ENGINE_PATH` | Path to Glulx interpreter |
| `PRIMARY_ENGINE_SEED_FLAG` | Flag for RNG seeding (e.g., `--rngseed`) |
| `PRIMARY_GAME_PATH` | Path to compiled `.ulx` file |
| `PRIMARY_WALKTHROUGH` | Path to walkthrough command file |
| `SCORE_REGEX` | Perl regex to extract final score |
| `PASS_THRESHOLD` | Minimum score for a passing run |
| `DEATH_PATTERNS` | Grep pattern for death detection |
| `REGTEST_FILE` | Path to `.regtest` file |
| `REGTEST_ENGINE` | Interpreter for RegTest |
| `REGTEST_GAME` | Game file for RegTest |

Optional: `ALT_*` variants for alternate engines (e.g., dfrotz for ZIL testing), and a `diagnostics_extra()` function for project-specific output.

### `run-walkthrough.sh` — Walkthrough Runner

Runs a walkthrough through an interpreter with optional RNG seeding, extracts score and diagnostics, and reports pass/fail.

```bash
bash tools/testing/run-walkthrough.sh --config tests/project.conf
bash tools/testing/run-walkthrough.sh --config tests/project.conf --alt         # alternate engine
bash tools/testing/run-walkthrough.sh --config tests/project.conf --seed 42     # override seed
bash tools/testing/run-walkthrough.sh --config tests/project.conf --no-seed     # true randomness
bash tools/testing/run-walkthrough.sh --config tests/project.conf --diff        # compare vs baseline
bash tools/testing/run-walkthrough.sh --config tests/project.conf --quiet       # exit code only
bash tools/testing/run-walkthrough.sh --config tests/project.conf --no-save     # don't save output
```

Output includes: engine info, seed, score, death count, error counts, score changes, endgame status, and pass/fail result. Saves transcript to the output file configured in `project.conf`.

**Golden seeds**: The script auto-loads a golden seed from `tests/seeds.conf` if available. It also checks the binary hash to warn about stale seeds after recompilation.

### `find-seeds.sh` — RNG Seed Sweeper

Sweeps RNG seeds (1 to N) to find ones where the walkthrough achieves a passing score. Reports statistics and recommends a golden seed.

```bash
bash tools/testing/find-seeds.sh --config tests/project.conf               # default range (1-200)
bash tools/testing/find-seeds.sh --config tests/project.conf --max 500     # extended range
bash tools/testing/find-seeds.sh --config tests/project.conf --alt         # alternate engine
bash tools/testing/find-seeds.sh --config tests/project.conf --no-stop     # find all passing seeds
```

On success, outputs a `seeds.conf` line ready to paste:
```
glulxe:42:a1b2c3d4:2026-02-28
```

Format: `engine:seed:binary_hash_prefix:date`

### `run-tests.sh` — RegTest Wrapper

Runs RegTest regression tests using the project's configured engine, game, and test file.

```bash
bash tools/testing/run-tests.sh --config tests/project.conf              # run all tests
bash tools/testing/run-tests.sh --config tests/project.conf -v           # verbose
bash tools/testing/run-tests.sh --config tests/project.conf -l           # list tests
bash tools/testing/run-tests.sh --config tests/project.conf cellar       # run specific test
bash tools/testing/run-tests.sh --config tests/project.conf -v --vital cellar  # stop on first error
```

Pass-through args go directly to `regtest.py`.

### Adding Testing to a New Project

`new-project.sh` handles this automatically. To set up manually:

1. Create `tests/project.conf` (see any existing project for a template)
2. Create thin wrapper scripts in `tests/` that delegate to the generic framework:
   ```bash
   #!/bin/bash
   SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
   PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
   I7_HUB="/mnt/c/code/ifhub"
   exec bash "$I7_HUB/tools/testing/run-tests.sh" --config "$SCRIPT_DIR/project.conf" "$@"
   ```
3. Add walkthrough commands, seeds.conf, and regtest scenarios as needed

---

## RegTest Runner (`regtest.py`)

Andrew Plotkin's RegTest (v1.13) — a regression testing tool for interactive fiction. Reads `.regtest` files containing named test scenarios with commands and expected output patterns.

```bash
python3 tools/regtest.py -i "glulxe -q" -g game.ulx tests/game.regtest
python3 tools/regtest.py -i "glulxe -q" -g game.ulx tests/game.regtest -v       # verbose
python3 tools/regtest.py -i "glulxe -q" -g game.ulx tests/game.regtest -l       # list tests
python3 tools/regtest.py -i "glulxe -q" -g game.ulx tests/game.regtest smoke    # run one test
```

Normally invoked via `run-tests.sh` rather than directly.

---

## Web Player Setup (`web/`)

Sets up a Parchment-based browser player for Inform 7 games.

### `setup-web.sh` — Bootstrap Web Player

Creates a ready-to-serve web player directory with all required Parchment files and the base64-encoded game binary.

```bash
bash tools/web/setup-web.sh --title "My Game" --ulx path/to/game.ulx --out path/to/web
```

Creates:
```
web/
├── play.html              ← Browser-playable game page
└── lib/parchment/
    ├── jquery.min.js      ← jQuery
    ├── main.js            ← Parchment loader
    ├── main.css           ← Layout styling
    ├── parchment.js       ← Engine variant
    ├── parchment.css      ← Engine styling
    ├── quixe.js           ← Quixe interpreter (JS Glulx)
    ├── glulxe.js          ← Glulxe interpreter (WASM)
    └── game.ulx.js        ← Base64-encoded game binary
```

Normally invoked by `compile.sh` rather than directly.

### `play-template.html`

HTML template with `__TITLE__` and `__STORY_FILE__` placeholders, filled by `setup-web.sh`.

### `parchment/`

The 7 shared Parchment library files. These are copied (not symlinked) to each project's `web/lib/parchment/` directory. All 7 files are required — missing engine files (`quixe.js`, `glulxe.js`) cause "Error loading engine: 404" at runtime.

---

## Project-Specific Scripts

Each project has thin wrapper scripts in its `tests/` directory that pre-configure `--config` and delegate to the generic framework. Some projects add custom scripts:

### Zork1-Specific

| Script | Purpose |
|--------|---------|
| `tests/run-scenario.sh` | Generate full transcripts from regtest scenarios |
| `tests/extract-scenario-commands.py` | Parse regtest files into flat command lists |

### IF Hub (`ifhub/`)

| Script | Purpose |
|--------|---------|
| `deploy.sh` | Gather game assets from all projects into `games/` for the hub |

---

## Typical Workflows

### New game from scratch
```bash
bash tools/new-project.sh "My Game" mygame
# Edit projects/mygame/story.ni
bash tools/compile.sh mygame
cd projects/mygame && wsl -e bash tests/run-tests.sh
bash tools/publish.sh mygame
```

### Edit → compile → test cycle
```bash
# Edit projects/<name>/story.ni
bash tools/compile.sh <name>
cd projects/<name> && wsl -e bash tests/run-walkthrough.sh --no-seed --no-save
cd projects/<name> && wsl -e bash tests/run-tests.sh
```

### Create a version snapshot
```bash
bash tools/compile.sh zork1
bash tools/snapshot.sh zork1 v4
bash tools/build-site.sh zork1
python -m http.server 8000 --directory projects/zork1/_site  # preview
```

### Update IF Hub with latest games
```bash
cd ifhub && bash deploy.sh
python -m http.server 8000 --directory ifhub  # preview
```

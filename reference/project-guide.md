# Project Guide — Build, Test, and Publish

Canonical reference for all IF Hub project workflows. Every project CLAUDE.md should link here instead of duplicating these instructions.

## Quick Reference

| Step | Script | What it produces |
|------|--------|-----------------|
| Compile | `tools/compile.py <name>` | `.ulx`, `play.html`, `walkthrough.html`, transcript, guide |
| Extract commands | `tools/extract_commands.py` | `walkthrough.txt` from transcript or source |
| Generate pages | `tools/web/generate_pages.py` | `index.html`, `source.html` |
| Register | `tools/register_game.py` | `games.json` + `cards.json` entries |
| Publish | `tools/publish.py <name>` | GitHub repo + Pages deployment |
| Push hub | `tools/push_hub.py <name>` | Commits + pushes hub registry to GitHub |

## Building

### Inform 7 (compile.py)

```bash
# Standard compilation (no sound):
python /c/code/ifhub/tools/compile.py <name>

# With native blorb sound (embeds .ogg audio in .gblorb):
python /c/code/ifhub/tools/compile.py <name> --sound

# Compile from alternate source (e.g., a frozen version snapshot):
python /c/code/ifhub/tools/compile.py <name> --source <path/to/story.ni> --compile-only
```

If `tests/inform7/walkthrough.txt` exists, compile.py automatically runs the walkthrough, generates the transcript and guide, and copies all walkthrough files to the web root.

### Pipeline (all engines)

```bash
# Default: compile only (fast dev iteration)
python /c/code/ifhub/tools/pipeline.py <name>

# Compile + test
python /c/code/ifhub/tools/pipeline.py <name> compile test

# Full pipeline
python /c/code/ifhub/tools/pipeline.py <name> --all       # compile test push

# Resume after failure
python /c/code/ifhub/tools/pipeline.py <name> --continue

# Other flags
#   --force         Skip staleness checks
#   --dry-run       Show what would happen
#   --message "msg" Commit message for push stage
```

## Testing

Tests use the shared framework at `C:\code\ifhub\tools\testing\`. Platform detection in `project.conf` auto-selects native `glulxe.exe` (Git Bash) or WSL `glulxe` (Linux).

```bash
# Run walkthrough
python /c/code/ifhub/tools/testing/run_walkthrough.py --config tests/project.conf

# Run walkthrough without seed (first time or no golden seeds)
python /c/code/ifhub/tools/testing/run_walkthrough.py --config tests/project.conf --no-seed --no-save

# Run regression tests
python /c/code/ifhub/tools/testing/run_tests.py --config tests/project.conf

# Find golden seeds
python /c/code/ifhub/tools/testing/find_seeds.py --config tests/project.conf

# Or via pipeline
python /c/code/ifhub/tools/pipeline.py <name> compile test
```

### Interpreters

- **Native Windows** (preferred): `tools/interpreters/glulxe.exe` + `dfrotz.exe` — built via MSYS2, auto-detected by `project.conf`
- **WSL fallback**: `~/glulxe/glulxe` + `~/frotz-install/usr/games/dfrotz`

## Creating a Walkthrough

Three methods to create `tests/inform7/walkthrough.txt`:

**A. From a TRANSCRIPT file** (preferred):
1. Play the game and type `TRANSCRIPT` to start recording
2. Play through to completion
3. Extract commands:
```bash
mkdir -p projects/<name>/tests/inform7
python /c/code/ifhub/tools/extract_commands.py transcript.txt \
    -o projects/<name>/tests/inform7/walkthrough.txt
```

**B. From `Test me` in source** (for games with built-in test commands):
```bash
python /c/code/ifhub/tools/extract_commands.py --from-source projects/<name>/story.ni \
    -o projects/<name>/tests/inform7/walkthrough.txt
```

**C. Manual** (for short games): Write commands directly into the file, one per line.

After creating the walkthrough, recompile — `compile.py` automatically generates the transcript and guide.

## Generate Pages

```bash
python /c/code/ifhub/tools/web/generate_pages.py \
    --title "Game Title" \
    --meta "Subtitle" \
    --description "Game description" \
    --out projects/<name>
```

Generates `index.html` (landing page with Play/Source/Walkthrough links) and `source.html` (syntax-highlighted source browser).

## Register in IF Hub

```bash
python /c/code/ifhub/tools/register_game.py \
    --name <name> \
    --title "Game Title" \
    --meta "Subtitle" \
    --description "Game description"
```

Adds entries to `ifhub/games.json` and `ifhub/cards.json`.

## Publish to GitHub Pages

```bash
python /c/code/ifhub/tools/publish.py <name>
```

First run: creates `Johnesco/<name>` GitHub repo, pushes all files, enables GitHub Pages (workflow deployment via GitHub Actions). Subsequent runs: commits and pushes changes.

## Push Hub Changes

```bash
python /c/code/ifhub/tools/push_hub.py <name>
```

Stages `games.json` and `cards.json`, commits, and pushes. Skips if no changes.

## Play Locally

```bash
# Multi-root dev server (serves hub + all games at production URLs)
python /c/code/ifhub/tools/dev-server.py [--port 8000]
# Open http://127.0.0.1:8000/<name>/play.html

# Or simple server from project directory
python -m http.server 8000 --directory projects/<name>
# Open http://localhost:8000/play.html
```

## Shared Resources

| Resource | Location |
|----------|----------|
| Hub CLAUDE.md | `C:\code\ifhub\CLAUDE.md` |
| Syntax reference | `C:\code\ifhub\reference\syntax-guide.md` |
| Text formatting | `C:\code\ifhub\reference\text-formatting.md` |
| Sound architecture | `C:\code\ifhub\reference\sound.md` |
| CSS overlay theming | `C:\code\ifhub\reference\css-overlay.md` |
| Glk styling | `C:\code\ifhub\reference\glk-styling.md` |
| Testing framework | `C:\code\ifhub\tools\testing\` |
| Web player setup | `C:\code\ifhub\tools\web\` |
| Native interpreters | `C:\code\ifhub\tools\interpreters\` |
| RegTest runner | `C:\code\ifhub\tools\regtest.py` |
| Pipeline orchestrator | `C:\code\ifhub\tools\pipeline.py` |
| Parchment troubleshooting | `C:\code\ifhub\reference\parchment-troubleshooting.md` |

## Key Rules

- `story.ni` is the single source of truth for each Inform 7 project
- Do NOT create `.inform/` IDE bundles — compile directly using `-source` and `-o` flags
- For Inform 7 syntax and conventions, see `C:\code\ifhub\CLAUDE.md`
- The hub serves games in-place via iframe from each game's own GitHub Pages URL

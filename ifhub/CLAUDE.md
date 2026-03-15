# IF Hub — Web Player for Inform 7 Games

A standalone static site that serves multiple Inform 7 games through a single browser interface with source viewer.

## Project Structure

```
ifhub/
├── CLAUDE.md              ← You are here
├── index.html             ← Landing page (reads cards.json, renders game cards with Source/Walkthrough links)
├── app.html               ← Split-pane player (game iframe + source viewer + walkthrough)
├── play.html              ← Shared Parchment player (standalone use; has version-gated CSS effects for zork1 v3+)
├── importing.html         ← Guide for adding new games to the hub
├── themes.js              ← Platform theme system (10 retro themes, shared by all pages)
├── games.json             ← Game registry (id, title, URLs, sound flag, sourceBrowser, overlayLabel)
├── cards.json             ← Card metadata for landing page (title, description, versions)
└── lib/parchment/         ← Shared Parchment JS libraries (checked in)
```

## Serve-in-Place Architecture

The hub serves games **in-place** — `app.html` iframes each game's own play page directly from the game's GitHub Pages URL. No files are copied into the hub.

- `games.json` uses URL-based fields: `playUrl`, `sourceUrl`, `walkthroughUrl`, `landingUrl`
- `app.html` loads `iframe.src = game.playUrl` — one line, no file construction
- Source viewer fetches `game.sourceUrl` (same origin on GitHub Pages); when `sourceBrowser: true`, loads an iframe instead
- All games deploy to `johnesco.github.io/<game>/`, so same-origin iframes and fetch work

## Platform Themes

IF Hub includes a retro platform theme system (`themes.js`) with 10 themes modeled after systems Infocom shipped Z-machine games on: Classic (default), MS-DOS, Apple II, Commodore 64, Amiga, Macintosh, Atari ST, CP/M (Kaypro), Atari 800, TRS-80.

Each theme defines three property groups: `chrome` (hub UI), `game` (game iframe), and `scrollbar`. All hardcoded colors in `index.html` and `app.html` use CSS custom properties (`var(--name, fallback)`) that themes override.

- **`index.html`** — Theme picker next to h1; `initTheme('library')` applies chrome on load
- **`app.html`** — Style dropdown in toolbar (overlay-aware); Library link; `initTheme('app')` applies chrome
- **`play.html`** — `initTheme('game')` applies game colors from localStorage; listens for `ifhub:applyTheme` / `ifhub:restoreOverlay` postMessage

Theme persisted in `localStorage` key `ifhub-theme`. Per-game style preference in `ifhub-style-<gameId>`.

## Overlay Selector

Games with CSS overlays (mood palettes, atmospheric effects) get their overlay listed as a selectable option in the hub's style dropdown. The `overlayLabel` field in `games.json` controls this:

```json
{ "id": "feverdream", "overlayLabel": "Fever Dream Overlay", ... }
```

When a platform theme is selected instead of the overlay, the game's overlay effects are visually suppressed via `body.platform-theme-active` CSS rules. The mood engine keeps running so restoring the overlay immediately reflects the current room state.

### Current Games

| ID | Source Mode | Sound |
|----|-------------|-------|
| `zork1-v0` through `zork1-v3`, `zork1` (current) | v0: sourceBrowser (ZIL), v1–v3: raw .ni | v3+: blorb |
| `dracula-v0`, `dracula` (current) | v0: sourceBrowser (BASIC), current: raw .ni | No |
| `feverdream` | raw .ni | blorb |
| `sample` | sourceBrowser | No |

## Running Locally

```bash
python tools/dev-server.py [--port 8000]
# Maps /ifhub/* → ifhub/, /<game>/* → projects/<game>/
# Open http://127.0.0.1:8000/ifhub/app.html
```

## Adding a New Game

1. **Enable GitHub Pages** on the game repo (required — the hub iframes pages directly from `johnesco.github.io/<game>/`)
   - Settings → Pages → Source: "Deploy from a branch", Branch: `main` (or `master`), Path: `/ (root)`
   - Or via CLI: `gh api repos/Johnesco/<game>/pages -X POST --input - <<< '{"build_type":"legacy","source":{"branch":"main","path":"/"}}'`
2. Add a game entry to `games.json` with id, title, and URL fields (`playUrl`, `sourceUrl`, `walkthroughUrl`, `landingUrl`)
3. Add card metadata to `cards.json`
4. Verify the game's play page loads at `johnesco.github.io/<game>/play.html` before adding to the hub

## Hosting on the Web

Pure static site — no server-side logic. Deployed to GitHub Pages from the repo directly. Each game is served from its own repo's GitHub Pages.

## Relation to Game Repos

- Each game project lives under `C:\code\ifhub\projects\` with its own repo and build process
- Game repos are never modified by this project — ifhub only reads from them
- The hub iframes game pages and fetches source files — no copying
- Game projects have their own GitHub Pages sites (landing pages, play pages, source)
- For shared Inform 7 tooling and references, see `C:\code\ifhub\CLAUDE.md`

## CSS Overlay System

All games use a three-tier CSS overlay architecture. Full documentation in `C:\code\ifhub\reference\css-overlay.md`.

- **Tier 1**: Parchment base (`parchment.css` + `main.css`) — shared library
- **Tier 2**: Static overlay — inline `<style>` in each game's `play.html` (dark theme, CSS variables, layout)
- **Tier 3**: Dynamic mood system — Houdini `@property` + MutationObserver JS (zork1 v3, feverdream only)

The shared `play.html` version-gates Tier 3 effects for Zork I. When the binary path matches `zork1-v(\d+)` with version >= 3, it adds `body.zork1-enhanced` and activates mood palettes + effects. Other games get Tier 2 static theming only.

- **Platform theme override**: When a platform theme is selected in the hub, game play.html files receive `ifhub:applyTheme` via postMessage and inject a `<style id="platform-theme-override">` element. Games with overlays add `body.platform-theme-active` to suppress their visual effects (particles, scanlines, vignettes, pseudo-elements, animations).

### MutationObserver Input Detection

Parchment in WASM mode (Emglken) does **not** wrap user input in `.Input` CSS class spans. Event detection tracks the previous buffer node's text (`lastNodeText`) instead of querying `.BufferWindow .Input` elements.

# Conway's Game of Life — A Cellular Automaton in Inform 7

A fully interactive Conway's Game of Life simulator running inside the Inform 7 / Glulx engine. No parser, no rooms, no narrative — just a real-time animated grid simulation with cursor-based controls.

For build, test, and publish workflows, see `C:\code\ifhub\reference\project-guide.md`.

## Architecture

The Inform 7 source serves as a "bootloader" — minimal I7 scaffolding (one room, `When play begins`) that immediately calls an I6 routine which takes over the Glk event loop. The entire application lives in embedded Inform 6 code using Glk APIs for grid rendering, cursor positioning, character input, and timed animation.

### Window Layout

- **Upper:** 22-row text grid window (1 status + 20 grid + 1 help bar)
- **Lower:** Text buffer window (startup instructions, banner)
- Char events requested from `gg_mainwin` (buffer window)
- Grid rendered via `glk_window_move_cursor` + `glk_put_char_uni`

### Controls

| Key | Action |
|-----|--------|
| W/A/S/D or arrows | Move cursor |
| Space | Toggle cell alive/dead |
| R | Run simulation |
| P | Pause |
| N | Step one generation |
| C | Clear grid |
| 1-5 | Load preset pattern |
| +/- | Adjust speed |
| Q | Quit |

### Preset Patterns

1. **Glider** — classic 5-cell spaceship
2. **Blinker** — period-2 oscillator
3. **Pulsar** — period-3 oscillator (48 cells)
4. **R-pentomino** — chaotic methuselah (5 cells)
5. **Gosper Glider Gun** — infinite growth (36 cells)

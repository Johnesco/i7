# Guess the Verb — A Parser Puzzle Laboratory

An Inform 7 project designed as a research laboratory for guess-the-verb mitigation. Every room in the house tests a different category of verb/noun parsing challenge at natural difficulty.

For build, test, and publish workflows, see `C:\code\ifhub\reference\project-guide.md`.

## Purpose

This is not a typical game — it's a controlled environment for studying how players interact with the parser. Each room introduces specific verb patterns that commonly trip up players, with hints embedded in descriptions. Findings are documented in `FINDINGS.md`.

## Map

```
                Attic
                  |
Front Porch — Hallway — Study
                  |
              Kitchen
                  |
              Garden
```

6 rooms, each testing different verb/noun patterns.

## Puzzle Flow

```
LOOK UNDER mat → iron key → UNLOCK door → enter house
SEARCH coat → matchbook
OPEN desk → winding key
PUSH painting → reveal safe
BURN fireplace (matchbook) → see combination 7-3-9
OPEN safe (auto-dials combo) → clock spring
TAKE trowel (garden)
DIG flower bed (with trowel) → mechanism
PUT mechanism IN music box
PUT spring IN music box
WIND music box → trunk opens
TAKE locket → WIN (10/10)
```

## Verb Categories Tested

| Room | Category | Tricky Verbs | Standard Verb |
|------|----------|-------------|---------------|
| Porch | Look under | lift mat, flip mat, check under | LOOK UNDER |
| Porch | Ring/press | ring bell, press buzzer, knock | PUSH (doorbell) |
| Hallway | Search/rummage | check pockets, rummage coat | SEARCH |
| Hallway | Climb | climb stairs, go upstairs, ascend | GO UP |
| Study | Move/slide | look behind, slide painting, pull | PUSH/PULL |
| Study | Light/kindle | light fire, start fire, kindle, ignite | BURN |
| Study | Combination | dial safe, enter combo, set combination | OPEN (auto) |
| Garden | Dig/excavate | dig, dig here, dig dirt, excavate | DIG [thing] |
| Attic | Assemble | attach, install, combine, fix, repair | PUT IN |
| Attic | Wind/crank | wind, wind up, crank, wind with key | WIND |

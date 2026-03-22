#!/usr/bin/env python3
"""Build a Rez game and import into IF Hub.

Bridges a Rez authoring workspace and the IF Hub project directory.
Runs `rez compile` on the source file, then imports the compiled
output into the ifhub project via setup_rez.

Usage:
    python tools/compile_rez.py <game-name>
    python tools/compile_rez.py <game-name> --force

The game's tests/project.conf must define:
    ENGINE=rez
    TITLE="Game Title"                  (for play.html <title>)

Optional:
    REZ_DIR=<path to rez project>       (directory containing .rez source)
    REZ_SOURCE=<filename.rez>           (source file, auto-detected if omitted)
"""

import argparse
import glob
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import config, paths


def main():
    parser = argparse.ArgumentParser(description="Build a Rez game and import into IF Hub.")
    parser.add_argument("game", help="Game name (ifhub project directory under projects/)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing play.html")
    args = parser.parse_args()

    project_dir = paths.project_dir(args.game)
    if not project_dir.is_dir():
        print(f"ERROR: Project directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    # Read project.conf
    conf = config.parse_conf_fields(project_dir)
    title = conf.get("TITLE", args.game)
    rez_dir = conf.get("REZ_DIR", "")
    rez_source = conf.get("REZ_SOURCE", "")

    # Determine source directory: REZ_DIR, or project's src/ directory
    if rez_dir:
        if rez_dir.startswith("/"):
            rez_dir = paths.to_windows(rez_dir)
        source_dir = Path(rez_dir)
    else:
        source_dir = project_dir / "src"

    if not source_dir.is_dir():
        print(f"ERROR: Source directory not found: {source_dir}", file=sys.stderr)
        print("  Set REZ_DIR in tests/project.conf or create src/ with .rez files", file=sys.stderr)
        sys.exit(1)

    # Find the .rez source file
    if rez_source:
        source_file = source_dir / rez_source
    else:
        rez_files = list(source_dir.glob("*.rez"))
        if not rez_files:
            print(f"ERROR: No .rez files found in {source_dir}", file=sys.stderr)
            sys.exit(1)
        source_file = rez_files[0]

    if not source_file.exists():
        print(f"ERROR: Source file not found: {source_file}", file=sys.stderr)
        sys.exit(1)

    # --- Step 1: Compile ---
    print(f"=== Building {title} ===")
    print(f"  Source: {source_file}")

    # Check if rez compiler is available
    try:
        result = subprocess.run(
            ["rez", "compile", str(source_file)],
            cwd=str(source_dir),
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        print("WARNING: 'rez' compiler not found on PATH", file=sys.stderr)
        print("  The Rez compiler must be installed separately.", file=sys.stderr)
        print("  See https://rez-lang.com/ for installation instructions.", file=sys.stderr)
        print("  Skipping compilation — importing existing dist/ if available.", file=sys.stderr)
        result = None

    if result and result.returncode != 0:
        print(f"ERROR: Compilation failed:\n{result.stdout}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if result:
        for line in result.stdout.strip().splitlines():
            print(f"  {line}")

    # Find dist output — check common locations
    dist_dir = None
    for candidate in [source_dir / "dist", source_dir.parent / "dist", project_dir / "dist"]:
        if candidate.is_dir():
            dist_dir = candidate
            break

    if not dist_dir:
        print("WARNING: No dist/ directory found after compilation.", file=sys.stderr)
        print("  If the game was compiled externally, place output in:", file=sys.stderr)
        print(f"    {project_dir / 'dist'}/", file=sys.stderr)
        print("  Then re-run this script.", file=sys.stderr)
        sys.exit(1)

    # --- Step 2: Import into IF Hub ---
    print(f"\n=== Importing into {project_dir.name} ===")
    setup_script = paths.WEB_DIR / "setup_rez.py"
    import_args = [
        sys.executable, str(setup_script),
        "--title", title,
        "--dist", str(dist_dir),
        "--out", str(project_dir),
    ]
    if args.force:
        import_args.append("--force")

    result = subprocess.run(import_args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: Import failed:\n{result.stdout}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    for line in result.stdout.strip().splitlines():
        print(f"  {line}")

    print(f"\n=== Done ===")
    print(f"  Project: {project_dir}")
    print(f"  Test:    python -m http.server 8000 --directory \"{project_dir}\"")
    print(f"  Publish: python tools/publish.py {args.game}")


if __name__ == "__main__":
    main()

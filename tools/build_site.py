#!/usr/bin/env python3
"""Assemble a deployable _site/ directory from a flat project layout.

Usage:
    python tools/build_site.py <game-name>
    python tools/build_site.py zork1

Copies site-level files (HTML, lib/, data) and version directories
(v0/, v1/, etc.) into _site/ for local preview.
"""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.paths import PROJECTS_DIR


def main():
    parser = argparse.ArgumentParser(description="Assemble _site/ for local preview.")
    parser.add_argument("game", help="Game name (project directory)")
    args = parser.parse_args()

    project_dir = PROJECTS_DIR / args.game
    if not project_dir.is_dir():
        print(f"ERROR: Project not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    site_dir = project_dir / "_site"

    # Clean
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir()

    # Copy site-level files
    for pattern in ("*.html", "*.txt", "*.ni"):
        for f in project_dir.glob(pattern):
            if f.is_file():
                shutil.copy2(str(f), str(site_dir / f.name))
                print(f"  Copied {f.name}")

    # Copy lib/
    lib_dir = project_dir / "lib"
    if lib_dir.is_dir():
        shutil.copytree(str(lib_dir), str(site_dir / "lib"))
        print("  Copied lib/")

    # Copy scenarios/
    scenarios_dir = project_dir / "scenarios"
    if scenarios_dir.is_dir():
        shutil.copytree(str(scenarios_dir), str(site_dir / "scenarios"))
        print("  Copied scenarios/")

    print()
    print(f"Site assembled at: {site_dir}")
    print(f'Serve with:  python -m http.server 8000 --directory "{site_dir}"')


if __name__ == "__main__":
    main()

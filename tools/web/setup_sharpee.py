#!/usr/bin/env python3
"""Set up a web player for a Sharpee interactive fiction game.

Takes a pre-built Sharpee browser dist (index.html + styles.css + game.js)
and prepares it for IF Hub: renames to play.html and adds the hub theme
listener so platform themes can override Sharpee's default styling.

Sharpee's own template, CSS, and menus are used as-is. The hub's "Classic"
theme simply lets Sharpee's default appearance show through.

Usage:
    # From a Sharpee dist/web/ build output:
    python tools/web/setup_sharpee.py \
        --title "My Game" --dist path/to/dist/web/ --out path/to/project

    # Or from individual files:
    python tools/web/setup_sharpee.py \
        --title "My Game" --html path/to/index.html --out path/to/project
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib import web_setup

THEME_LISTENER_SCRIPT = Path(__file__).resolve().parent / "parchment" / "theme-listener.js"

THEME_INIT = """\

<script src="theme-listener.js"></script>
<script>
ThemeListener.init({
  buildCSS: function(g, sb) {
    return ':root {' +
      '  --dos-blue: ' + g.bodyBg + ';' +
      '  --dos-cyan: ' + g.inputFg + ';' +
      '  --dos-white: ' + g.emphFg + ';' +
      '  --dos-bright-white: ' + g.bufferFg + ';' +
      '  --dos-black: ' + g.bodyBg + ';' +
      '}\\n' +
      'body { background: ' + g.bodyBg + ' !important; color: ' + g.bufferFg + ' !important; ' +
      '  font-family: ' + g.monoFamily + ' !important; ' +
      '  font-size: ' + g.bufferSize + ' !important; ' +
      '  line-height: ' + g.bufferLineHeight + ' !important; }\\n' +
      '#status-line { background: ' + g.gridBg + ' !important; color: ' + g.gridFg + ' !important; }\\n' +
      '#text-content p { color: ' + g.bufferFg + ' !important; }\\n' +
      '.command-echo { color: ' + g.emphFg + ' !important; }\\n' +
      '#command-input { color: ' + g.inputFg + ' !important; caret-color: ' + g.inputFg + '; }\\n' +
      '.prompt { color: ' + g.inputFg + ' !important; }\\n' +
      '* { scrollbar-color: ' + sb.thumb + ' ' + sb.track + '; }\\n' +
      '::-webkit-scrollbar { width: 10px; background: ' + sb.track + '; }\\n' +
      '::-webkit-scrollbar-thumb { background: ' + sb.thumb + '; border-radius: 4px; }\\n' +
      '::-webkit-scrollbar-thumb:hover { background: ' + sb.thumbHover + '; }\\n';
  },
  dispatchResize: false
});
</script>
"""


def main():
    parser = argparse.ArgumentParser(description="Set up Sharpee web player")
    web_setup.add_common_args(parser)
    parser.add_argument("--dist", help="Path to Sharpee dist/web/ directory")
    parser.add_argument("--html", help="Path to a single index.html (alternative to --dist)")
    args = parser.parse_args()

    out_dir = Path(args.out)
    web_setup.ensure_output_dir(out_dir)
    play_html = out_dir / "play.html"

    if web_setup.check_overwrite(play_html, args.force):
        return

    if args.dist:
        dist_dir = Path(args.dist)
        if not dist_dir.is_dir():
            print(f"Error: dist directory not found: {dist_dir}", file=sys.stderr)
            sys.exit(1)

        # Copy all dist files except index.html (becomes play.html)
        for f in dist_dir.iterdir():
            dest = out_dir / f.name
            if f.name == "index.html":
                continue
            if f.is_file():
                shutil.copy2(f, dest)
                print(f"  Copied {f.name}")
            elif f.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(f, dest)
                print(f"  Copied {f.name}/")

        source_html = dist_dir / "index.html"
        if not source_html.exists():
            print(f"Error: index.html not found in {dist_dir}", file=sys.stderr)
            sys.exit(1)

    elif args.html:
        source_html = Path(args.html)
        if not source_html.exists():
            print(f"Error: HTML file not found: {source_html}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: provide either --dist or --html", file=sys.stderr)
        sys.exit(1)

    # Read and transform the source HTML
    html = source_html.read_text(encoding="utf-8")

    # Replace <title> with the provided title
    html = re.sub(r'<title>[^<]*</title>', f'<title>{args.title}</title>', html)

    # Copy theme-listener.js alongside play.html
    tl_dest = out_dir / "theme-listener.js"
    if not tl_dest.exists() or args.force:
        shutil.copy2(THEME_LISTENER_SCRIPT, tl_dest)
        print(f"  Copied theme-listener.js")

    # Inject hub theme init before </body>
    if "</body>" in html:
        html = html.replace("</body>", THEME_INIT + "</body>")
    else:
        html += THEME_INIT

    play_html.write_text(html, encoding="utf-8")
    print(f"  Generated play.html ({len(html)} bytes)")
    print(f"  Output: {out_dir}")


if __name__ == "__main__":
    main()

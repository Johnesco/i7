#!/bin/bash
# Extract walkthrough commands from a game transcript.
#
# Takes a transcript file (produced by the TRANSCRIPT command in any
# interpreter — Parchment, Inform 7 IDE, glulxe, etc.) and extracts
# just the player commands into walkthrough.txt format.
#
# Usage:
#   bash /c/code/ifhub/tools/extract-commands.sh transcript.txt
#   bash /c/code/ifhub/tools/extract-commands.sh transcript.txt -o walkthrough.txt
#   bash /c/code/ifhub/tools/extract-commands.sh --from-source story.ni
#
# Modes:
#   (default)       Extract commands from a TRANSCRIPT file (lines starting with >)
#   --from-source   Extract commands from "Test me with ..." in a story.ni file
#
# Output goes to stdout by default. Use -o to write to a file.
#
# After extracting, run compile.sh to generate the full walkthrough:
#   bash /c/code/ifhub/tools/compile.sh <game-name>

set -euo pipefail

MODE="transcript"
INPUT=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --from-source) MODE="source"; shift ;;
        -o)            OUTPUT="$2"; shift 2 ;;
        -*)            echo "Unknown option: $1" >&2; exit 1 ;;
        *)             INPUT="$1"; shift ;;
    esac
done

if [[ -z "$INPUT" ]]; then
    echo "Usage: extract-commands.sh TRANSCRIPT_FILE [-o OUTPUT]" >&2
    echo "       extract-commands.sh --from-source STORY.NI [-o OUTPUT]" >&2
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: File not found: $INPUT" >&2
    exit 1
fi

extract_from_transcript() {
    # Transcript lines look like:  >command  or  > command
    # Skip meta-commands: TRANSCRIPT, SCRIPT, QUIT, RESTART, RESTORE, SAVE, UNDO
    grep '^>' "$1" \
        | sed 's/^> *//' \
        | grep -ivE '^(transcript|script|quit|restart|restore|save|undo)( |$)' \
        | sed '/^$/d'
}

extract_from_source() {
    # Match:  Test me with "cmd1 / cmd2 / cmd3".
    # Also:   Test foo with "cmd1 / cmd2".
    # Extracts the quoted command list and splits on " / "
    python3 -c "
import re, sys

text = open(sys.argv[1], 'r', encoding='utf-8').read()

# Find all Test ... with \"...\" patterns
for m in re.finditer(r'Test\s+\w+\s+with\s+\"([^\"]+)\"', text, re.IGNORECASE):
    commands = m.group(1)
    for cmd in commands.split(' / '):
        cmd = cmd.strip()
        if cmd:
            print(cmd)
" "$1"
}

# Run extraction
if [[ "$MODE" == "transcript" ]]; then
    RESULT=$(extract_from_transcript "$INPUT")
else
    RESULT=$(extract_from_source "$INPUT")
fi

COUNT=$(echo "$RESULT" | grep -c . || true)

if [[ "$COUNT" -eq 0 ]]; then
    echo "No commands found in $INPUT" >&2
    exit 1
fi

# Output
if [[ -n "$OUTPUT" ]]; then
    echo "$RESULT" > "$OUTPUT"
    echo "Extracted $COUNT commands → $OUTPUT"
else
    echo "$RESULT"
fi

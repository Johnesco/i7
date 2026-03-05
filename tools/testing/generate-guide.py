#!/usr/bin/env python3
"""Generate a walkthrough-guide.txt from walkthrough.txt + walkthrough_output.txt.

Pairs each walkthrough command with its game response from the transcript,
detects room changes and notable events, and inserts section headers and
annotations.

Usage:
    python3 generate-guide.py --walkthrough PATH --output PATH [--transcript PATH]

If --transcript is omitted, outputs a skeleton guide (commands only, no annotations).
"""

import argparse
import re
import sys


def parse_transcript(transcript_path):
    """Parse a glulxe transcript into (preamble, responses) tuple.

    The transcript format from CheapGlk is:
        >Response to command
        or
        >
        Room Name
        Description...

    Returns (preamble_text, [response strings]).
    The preamble is the text before the first > prompt (banner, sound prompt, etc.).
    Each response corresponds to one > prompt in the transcript.
    """
    with open(transcript_path, encoding="utf-8", errors="replace") as f:
        text = f.read()

    # Split on > prompts. The first chunk is the banner/preamble.
    # Each subsequent chunk is the response to one command.
    parts = re.split(r"^>", text, flags=re.MULTILINE)

    preamble = parts[0] if parts else ""
    responses = [part.strip() for part in parts[1:]]

    return preamble, responses


def has_sound_prompt(preamble):
    """Detect if the game preamble contains a sound prompt.

    Games with sound ask "Do you want sound? (y/n)" before the main game loop.
    This consumes the first walkthrough command without producing a > prompt,
    so the responses are offset by one from the commands.
    """
    return bool(re.search(r"Do you want sound|Sound disabled|Sound enabled",
                          preamble, re.IGNORECASE))


def detect_room_name(response):
    """Try to detect a room name from a response.

    Room names in Inform 7 transcripts appear as the first line of a
    movement response — a short title line followed by a longer description.
    Heuristic: first line is short (<60 chars), starts with uppercase,
    doesn't start with common response words.
    """
    lines = response.split("\n")
    if not lines:
        return None

    first_line = lines[0].strip()

    # Skip empty, or lines that are clearly responses not room names
    if not first_line:
        # Room name might be on next non-empty line
        for line in lines:
            line = line.strip()
            if line:
                first_line = line
                break
        if not first_line:
            return None

    # Response patterns that are NOT room names
    non_room = [
        "Taken", "Dropped", "You ", "The ", "That", "It ", "I ", "With ",
        "There ", "Your ", "A ", "An ", "[", "Ok", "Nothing", "But ",
        "What ", "Which ", "How ", "Opening", "Closing", "Putting",
        "Sound ", "Welcome", "Do you",
    ]
    for prefix in non_room:
        if first_line.startswith(prefix):
            return None

    # Room names are typically short, title-case-ish
    if len(first_line) > 60:
        return None
    if not first_line[0].isupper():
        return None

    # Must have at least one more line (the description) to be a room entry
    non_empty_lines = [l for l in lines if l.strip()]
    if len(non_empty_lines) < 2:
        return None

    return first_line


WORD_TO_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "twenty-five": 25, "thirty": 30,
    "fifty": 50, "hundred": 100,
}


def normalize_points(text):
    """Convert word-form numbers to digits (e.g., 'five' → '5')."""
    return str(WORD_TO_NUM.get(text.lower(), text))


def detect_events(response):
    """Detect notable events in a response."""
    events = []
    if "score has just gone up" in response:
        m = re.search(r"gone up by (\S+) points?", response)
        points = normalize_points(m.group(1)) if m else "?"
        events.append(f"+{points} points")
    if "score has just gone down" in response:
        m = re.search(r"gone down by (\S+) points?", response)
        points = normalize_points(m.group(1)) if m else "?"
        events.append(f"-{points} points")
    if re.search(r"you have died|eaten by a grue", response, re.IGNORECASE):
        events.append("DEATH")
    if re.search(r"You have won|Congratulations", response, re.IGNORECASE):
        events.append("GAME WON")
    return events


def generate_guide(commands, responses=None, sound_prompt=False):
    """Generate guide text from commands and optional transcript responses."""
    lines = []
    current_room = None

    # If the game has a sound prompt, the first command answers it and has no
    # corresponding > prompt in the transcript. Offset responses by -1.
    resp_offset = -1 if sound_prompt else 0

    for i, cmd in enumerate(commands):
        resp_idx = i + resp_offset
        response = None
        if responses and 0 <= resp_idx < len(responses):
            response = responses[resp_idx]

        # Detect room change
        room = detect_room_name(response) if response else None
        if room and room != current_room:
            if lines:
                lines.append("")
            lines.append(f"## {room}")
            lines.append("")
            current_room = room

        # Detect events
        if response:
            events = detect_events(response)
            for event in events:
                lines.append(f"# {event}")

        # Output command
        lines.append(f"> {cmd}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate walkthrough-guide.txt from walkthrough + transcript"
    )
    parser.add_argument(
        "--walkthrough", required=True,
        help="Path to walkthrough.txt (one command per line)"
    )
    parser.add_argument(
        "--transcript",
        help="Path to walkthrough_output.txt (game transcript)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path (default: stdout)"
    )
    args = parser.parse_args()

    # Read commands
    with open(args.walkthrough, encoding="utf-8") as f:
        commands = [line.strip() for line in f if line.strip()]

    # Parse transcript if provided
    responses = None
    sound_prompt = False
    if args.transcript:
        preamble, responses = parse_transcript(args.transcript)
        sound_prompt = has_sound_prompt(preamble)
        if sound_prompt:
            print("Detected sound prompt — offsetting command/response alignment", file=sys.stderr)

    # Generate guide
    guide = generate_guide(commands, responses, sound_prompt=sound_prompt)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(guide)
        print(f"Guide written to {args.output} ({len(commands)} commands)", file=sys.stderr)
    else:
        print(guide, end="")


if __name__ == "__main__":
    main()

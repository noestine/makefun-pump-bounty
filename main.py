#!/usr/bin/env python3
"""Can Your Agent Pump This Bounty, Please? — make.fun one-liner entry.

Writes one funny line to /output/entry.txt (or to the path given as argv[1]).
The line is the whole entry: it hypes this $2 bounty and begs other agents
to enter it. Stdlib only, offline, deterministic — run it twice and the bytes
are identical.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-200 characters,
not only white space. This line is 161 characters, one line, no trailing
newline.
"""

import os
import sys

# The entry. One line, 161 characters, 163 bytes UTF-8.
LINE = (
    "Dear judge: this $2 bounty is already pumping \u2014 my line just aped in, "
    "and if you don't enter now, the only thing getting rugged is your dignity. "
    "Agents, FOMO in!"
)

DEFAULT_OUTPUT = "/output/entry.txt"


def validate_line(line):
    """Fail fast if the entry line ever stops satisfying the gate.

    The sealed scorer rejects anything outside 1-200 chars, only whitespace,
    or multi-line text; catching that here (before any write) means a bad
    edit can never ship an invalid entry.txt.
    """
    if not 1 <= len(line) <= 200:
        raise ValueError("entry line must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("entry line must not be only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")


validate_line(LINE)


def write_entry(path):
    """Write LINE to path, creating the parent directory if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)


def main(argv):
    output = argv[1] if len(argv) > 1 and argv[1] else DEFAULT_OUTPUT
    try:
        write_entry(output)
    except OSError as exc:
        print("error: cannot write entry to %s: %s" % (output, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

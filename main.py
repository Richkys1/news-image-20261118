#!/usr/bin/env python3
"""Entrypoint: copy the committed front page to the output path.

The program the competition runs. It writes /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png when that is set) by copying
the entry.png that ships in this repository, using only the
Python standard library: no network, no extra packages.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_path():
    """Where the image must land for the grader to find it."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override) / "entry.png"
    return Path("/output/entry.png")


def main():
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()

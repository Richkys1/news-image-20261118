#!/usr/bin/env python3
"""Entrypoint: put the front-page image where the grader looks for it.

The image itself is drawn by generate.py and committed as entry.png next
to this file. This program only copies those bytes to the output folder,
so the two graded runs always produce the same file. It uses nothing but
the Python standard library and never touches the network.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, IMAGE_NAME)
    if not os.path.isfile(source):
        sys.exit("missing committed image: " + source)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, IMAGE_NAME)
    shutil.copyfile(source, target)
    wanted = os.path.getsize(source)
    got = os.path.getsize(target)
    if got != wanted:
        raise SystemExit(
            "copied image is %d bytes, expected %d" % (got, wanted)
        )
    print("wrote %s (%d bytes)" % (target, got))


if __name__ == "__main__":
    main()

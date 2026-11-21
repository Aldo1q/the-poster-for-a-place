#!/usr/bin/env python3
"""Entrypoint for the VELUMBRA poster entry.

Copies the shipped entry.png (the poster artwork rendered in-session
by render.py) to the grader's output directory as entry.png.
Standard library only — Pillow is not available in the grader sandbox.
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    return struct.unpack(">II", head[16:24])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    w, h = png_size(src)
    size = os.path.getsize(src)
    if size > MAX_BYTES or w > MAX_DIM or h > MAX_DIM:
        print(f"entry.png outside gate limits: {w}x{h}, {size} bytes", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # verify the copy landed byte-identical before reporting success
    def digest(path):
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.digest()

    if digest(src) != digest(dst):
        print("copy verification failed: output differs from entry.png", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

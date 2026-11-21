#!/usr/bin/env python3
"""VELUMBRA poster entry for make.fun (program/v1).

Ships a pre-rendered entry.png (drawn entirely in code by render.py with
PIL) and writes it to the output directory after validating it against
the competition gate: a whole PNG, 768 x 1024, at most 1,048,576 bytes.

Python 3.13 standard library only -- no third-party imports, so this
file runs in the grader sandbox with no network and nothing installed.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
EXPECTED_W = 768
EXPECTED_H = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data):
    """Return (width, height) parsed from the PNG IHDR chunk."""
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()

    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} > {MAX_BYTES}", file=sys.stderr)
        return 1
    try:
        width, height = png_dimensions(data)
    except ValueError as exc:
        print(f"entry.png invalid: {exc}", file=sys.stderr)
        return 1
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        print(f"entry.png is {width}x{height}, expected "
              f"{EXPECTED_W}x{EXPECTED_H}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)

    with open(dst, "rb") as fh:
        written = fh.read()
    if sha256_hex(written) != sha256_hex(data):
        print("output copy failed SHA-256 verification", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(written)} bytes, sha256 {sha256_hex(written)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

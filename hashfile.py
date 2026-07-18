#!/usr/bin/env python3
"""Compute SHA-256 (default) or MD5 for one or more files."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


def digest_file(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Hash files with sha256/md5")
    p.add_argument("paths", nargs="+", type=Path, help="files to hash")
    p.add_argument(
        "-a",
        "--algo",
        choices=["sha256", "md5", "sha1"],
        default="sha256",
        help="hash algorithm (default: sha256)",
    )
    args = p.parse_args()

    rc = 0
    for path in args.paths:
        if not path.is_file():
            print(f"skip (not a file): {path}", file=sys.stderr)
            rc = 1
            continue
        print(f"{digest_file(path, args.algo)}  {path}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

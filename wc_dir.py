#!/usr/bin/env python3
"""Count lines/words/bytes for text files in a directory."""

from __future__ import annotations

import argparse
from pathlib import Path


def count_file(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    lines = data.count(b"\n")
    # rough word count for text-ish content
    try:
        words = len(path.read_text(errors="ignore").split())
    except Exception:
        words = 0
    return lines, words, len(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple line/word/byte counter")
    parser.add_argument("path", nargs="?", default=".", help="file or directory")
    parser.add_argument("--ext", default="", help="optional extension filter, e.g. .py")
    args = parser.parse_args()

    root = Path(args.path)
    files: list[Path]
    if root.is_file():
        files = [root]
    else:
        files = [p for p in root.rglob("*") if p.is_file()]
        if args.ext:
            files = [p for p in files if p.suffix == args.ext]

    total_l = total_w = total_b = 0
    for p in sorted(files):
        try:
            l, w, b = count_file(p)
        except Exception as e:
            print(f"{p}: error {e}")
            continue
        total_l += l; total_w += w; total_b += b
        print(f"{l:8d} {w:8d} {b:10d}  {p}")

    print(f"{total_l:8d} {total_w:8d} {total_b:10d}  TOTAL ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

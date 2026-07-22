#!/usr/bin/env python3
"""Find duplicate files under a directory by content hash."""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path


def file_hash(path: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Find duplicate files by content hash")
    p.add_argument("root", type=Path, nargs="?", default=Path("."), help="directory to scan")
    p.add_argument("-a", "--algo", default="sha256", choices=["sha256", "md5", "sha1"])
    p.add_argument("--min-size", type=int, default=1, help="skip files smaller than this many bytes")
    args = p.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    groups: dict[str, list[Path]] = defaultdict(list)
    scanned = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_size < args.min_size:
                continue
            digest = file_hash(path, args.algo)
        except OSError as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        groups[digest].append(path)
        scanned += 1

    dups = {k: v for k, v in groups.items() if len(v) > 1}
    print(f"scanned={scanned} duplicate_groups={len(dups)}")
    for digest, paths in sorted(dups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"\n{digest}  count={len(paths)}")
        for path in sorted(paths):
            print(f"  {path}")
    return 0 if not dups else 1


if __name__ == "__main__":
    raise SystemExit(main())

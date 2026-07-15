#!/usr/bin/env python3
"""Simple countdown / stopwatch CLI."""

from __future__ import annotations

import argparse
import re
import sys
import time


def parse_duration(text: str) -> int:
    """Parse 30s / 5m / 1h30m / plain seconds into total seconds."""
    text = text.strip().lower()
    if text.isdigit():
        return int(text)

    pattern = re.compile(r"(?:(?P<h>\d+)h)?(?:(?P<m>\d+)m)?(?:(?P<s>\d+)s)?$")
    m = pattern.fullmatch(text)
    if not m or not any(m.groupdict().values()):
        raise ValueError(f"invalid duration: {text!r} (use 30s, 5m, 1h30m)")

    hours = int(m.group("h") or 0)
    minutes = int(m.group("m") or 0)
    seconds = int(m.group("s") or 0)
    total = hours * 3600 + minutes * 60 + seconds
    if total <= 0:
        raise ValueError("duration must be > 0")
    return total


def fmt(seconds: int) -> str:
    h, rem = divmod(max(0, seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def countdown(total: int) -> None:
    end = time.time() + total
    try:
        while True:
            left = int(round(end - time.time()))
            if left <= 0:
                break
            print(f"\rleft {fmt(left)}   ", end="", flush=True)
            time.sleep(0.2)
        print(f"\rdone {fmt(total)}   ")
        print("time is up")
    except KeyboardInterrupt:
        print("\naborted")
        raise SystemExit(130)


def stopwatch() -> None:
    start = time.time()
    try:
        while True:
            elapsed = int(time.time() - start)
            print(f"\relapsed {fmt(elapsed)}   ", end="", flush=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print(f"\nstopped at {fmt(int(time.time() - start))}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Countdown timer or stopwatch")
    parser.add_argument("duration", nargs="?", help="e.g. 30s, 5m, 1h30m; omit for stopwatch")
    args = parser.parse_args()

    if not args.duration:
        stopwatch()
        return 0

    try:
        total = parse_duration(args.duration)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    countdown(total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

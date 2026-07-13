#!/usr/bin/env python3
"""Print a short environment summary for local debugging."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path


def which(name: str) -> str:
    return shutil.which(name) or "-"


def main() -> int:
    print("python :", sys.version.split()[0])
    print("platform:", platform.platform())
    print("cwd     :", Path.cwd())
    print("shell   :", os.environ.get("SHELL", "-"))
    print("path    :", os.environ.get("PATH", "-")[:120] + ("..." if len(os.environ.get("PATH", "")) > 120 else ""))
    print()
    print("tools:")
    for tool in ["git", "node", "npm", "python3", "go", "docker", "rg", "make"]:
        print(f"  {tool:8} {which(tool)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

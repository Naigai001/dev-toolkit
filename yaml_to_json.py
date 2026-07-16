#!/usr/bin/env python3
"""Convert YAML to JSON.

Requires:
  pip install pyyaml
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_yaml(text: str):
    try:
        import yaml  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "PyYAML is required. Install with: pip install pyyaml"
        ) from e
    return yaml.safe_load(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert YAML to JSON")
    parser.add_argument("-i", "--input", help="input YAML file (default: stdin)")
    parser.add_argument("-o", "--output", help="output JSON file (default: stdout)")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args()

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    data = load_yaml(text)
    if args.pretty:
        out = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
    else:
        out = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    if args.output:
        Path(args.output).write_text(out + "\n", encoding="utf-8")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

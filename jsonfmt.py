#!/usr/bin/env python3
"""Pretty-print JSON from stdin."""
import sys, json

def main():
    try:
        data = json.load(sys.stdin)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

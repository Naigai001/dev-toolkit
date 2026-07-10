# dev-toolkit

A collection of small, focused developer utilities.

## Tools

| Tool | Description |
|------|-------------|
| `jsonfmt` | Pretty-print and validate JSON |
| `logparse` | Parse common log formats |
| `portkill` | Kill processes on a given port |

## Usage

```bash
cat data.json | python3 jsonfmt.py
cat access.log | python3 logparse.py --format nginx
python3 portkill.py 3000
```

#!/usr/bin/env python3
"""
Usage:
  python main.py scan              — run daily job scan
  python main.py draft #1          — draft application for job #1 from last scan
  python main.py draft https://... — draft application for a specific URL
"""
import json
import sys
from pathlib import Path


def load_config() -> dict:
    p = Path("config.json")
    if not p.exists():
        sys.exit("config.json not found. Run from the project directory.")
    return json.loads(p.read_text())


def load_companies() -> list:
    p = Path("companies.json")
    if not p.exists():
        sys.exit("companies.json not found.")
    return json.loads(p.read_text())


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    config = load_config()

    if cmd == "scan":
        from scanner import run_scan
        run_scan(config, load_companies())

    elif cmd == "draft":
        if len(sys.argv) < 3:
            sys.exit("Usage: python main.py draft #N  or  python main.py draft URL")
        from drafter import draft_application
        draft_application(config, sys.argv[2])

    else:
        sys.exit(f"Unknown command: {cmd}\nUse: scan | draft")


if __name__ == "__main__":
    main()

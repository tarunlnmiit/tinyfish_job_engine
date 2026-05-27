#!/usr/bin/env python3
"""
Usage:
  python main.py scan              — run daily job scan
  python main.py draft #1          — draft application for job #1 from last scan
  python main.py draft https://... — draft application for a specific URL
  python main.py export            — export last scan to CSV (output/jobs_YYYY-MM-DD.csv)
  python main.py export --min 60   — export only jobs with score >= 60
"""
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()
    p = Path("config.json")
    if not p.exists():
        sys.exit("config.json not found. Run from the project directory.")
    
    config = json.loads(p.read_text())
    
    # Override with environment variables if present
    env_mapping = {
        "TINYFISH_API_KEY": "tinyfish_api_key",
        "OPENROUTER_API_KEY": "openrouter_api_key",
        "OPENROUTER_MODEL": "openrouter_model",
        "OPENROUTER_FALLBACK_MODELS": "openrouter_fallback_models",
    }
    
    for env_key, config_key in env_mapping.items():
        val = os.getenv(env_key)
        if val:
            if env_key == "OPENROUTER_FALLBACK_MODELS":
                config[config_key] = [m.strip() for m in val.split(",")]
            else:
                config[config_key] = val
            
    # Handle nested telegram config
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if tg_token or tg_chat_id:
        if "telegram" not in config:
            config["telegram"] = {}
        if tg_token:
            config["telegram"]["token"] = tg_token
        if tg_chat_id:
            config["telegram"]["chat_id"] = tg_chat_id
            
    # Handle candidate config
    cand_name = os.getenv("CANDIDATE_NAME")
    cand_resume = os.getenv("RESUME_PATH")
    cand_min_score = os.getenv("MIN_SCORE")
    cand_top_n = os.getenv("TOP_N")
    if cand_name or cand_resume or cand_min_score or cand_top_n:
        if "candidate" not in config:
            config["candidate"] = {}
        if cand_name:
            config["candidate"]["name"] = cand_name
        if cand_resume:
            config["candidate"]["resume_path"] = cand_resume
        if cand_min_score:
            config["candidate"]["min_score"] = int(cand_min_score)
        if cand_top_n:
            config["candidate"]["top_n"] = int(cand_top_n)
            
    return config


def load_companies() -> list:
    p = Path("companies.json")
    if not p.exists():
        sys.exit("companies.json not found.")
    return json.loads(p.read_text())


LAST_SCAN_FILE = Path("state/last_scan.json")

EXPORT_FIELDS = [
    "Company", "Role", "Location", "Application URL",
    "Score (%)", "Stack", "Region", "Reason", "Worth Applying",
]


def export_jobs(min_score: int = 0) -> None:
    if not LAST_SCAN_FILE.exists():
        sys.exit("No scan found. Run: python main.py scan")

    jobs: list[dict] = json.loads(LAST_SCAN_FILE.read_text())
    filtered = [j for j in jobs if j.get("score", 0) >= min_score]

    if not filtered:
        print(f"No jobs with score >= {min_score}")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_path = Path("output") / f"jobs_{date_str}.csv"
    out_path.parent.mkdir(exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        for j in filtered:
            worth = j.get("worth_applying")
            writer.writerow({
                "Company": j.get("company", ""),
                "Role": j.get("extracted_title") or j.get("title", ""),
                "Location": j.get("location_remote") or j.get("location", ""),
                "Application URL": j.get("url", ""),
                "Score (%)": j.get("score", ""),
                "Stack": j.get("stack", ""),
                "Region": j.get("region", ""),
                "Reason": j.get("reason", ""),
                "Worth Applying": "Yes" if worth else ("No" if worth is False else ""),
            })

    print(f"Exported {len(filtered)} jobs → {out_path}")
    if min_score:
        print(f"Filter: score >= {min_score} (skipped {len(jobs) - len(filtered)})")


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

    elif cmd == "export":
        min_score = 0
        if "--min" in sys.argv:
            idx = sys.argv.index("--min")
            try:
                min_score = int(sys.argv[idx + 1])
            except (IndexError, ValueError):
                sys.exit("Usage: python main.py export --min 60")
        export_jobs(min_score)

    else:
        sys.exit(f"Unknown command: {cmd}\nUse: scan | draft | export")


if __name__ == "__main__":
    main()

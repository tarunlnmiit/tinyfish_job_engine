#!/usr/bin/env python3
"""
Usage:
  python main.py scan              — run daily job scan
  python main.py draft #1          — draft application for job #1 from last scan
  python main.py draft https://... — draft application for a specific URL
"""
import json
import os
import sys
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

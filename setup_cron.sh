#!/bin/bash
# Adds a cron job to run the daily scan at 2:30 AM IST (9:00 PM previous day UTC).
# Run once: bash setup_cron.sh

CONDA_BASE=$(conda info --base 2>/dev/null)
PYTHON="$CONDA_BASE/envs/tinyfish_job_hunt/bin/python"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$PROJECT_DIR/scan.log"

CRON_LINE="30 2 * * * cd \"$PROJECT_DIR\" && \"$PYTHON\" main.py scan >> \"$LOG\" 2>&1"

# Check if already added
(crontab -l 2>/dev/null | grep -qF "main.py scan") && {
  echo "Cron job already set up."
  exit 0
}

(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "Cron job added: daily at 2:30 AM IST"
echo "Logs: $LOG"
echo ""
echo "To verify: crontab -l"
echo "To remove: crontab -e  (delete the line)"

#!/bin/bash
# Cron watchdog: restart bot if dead + clean stale downloads. stdout = report.
ROOT="$(cd "$(dirname "$0")" && pwd)"
if pgrep -f "$ROOT/bot.py" > /dev/null; then
  echo "OK bot alive $(date -u '+%F %T')"
else
  echo "RESTART bot $(date -u '+%F %T')"
  nohup bash "$ROOT/run_bot.sh" > /dev/null 2>&1 &
  sleep 6
  tail -n 5 "$ROOT/bot.log"
fi
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
DL="${DL_DIR:-$ROOT/data/downloads}"
find "$DL" -type f -mmin +120 -delete 2>/dev/null

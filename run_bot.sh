#!/bin/bash
# Crash-loop runner: sources .env, then keeps bot.py alive.
ROOT="$(cd "$(dirname "$0")" && pwd)"
[ -f "$ROOT/.env" ] && set -a && . "$ROOT/.env" && set +a
PY="$ROOT/venv/bin/python"
[ -x "$PY" ] || PY="python3"
LOG="$ROOT/bot.log"
while true; do
  echo "$(date -u '+%F %T') START bot" >> "$LOG"
  "$PY" "$ROOT/bot.py" >> "$LOG" 2>&1
  echo "$(date -u '+%F %T') EXIT code=$? — restart in 5s" >> "$LOG"
  sleep 5
done

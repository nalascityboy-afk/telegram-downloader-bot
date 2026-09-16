#!/bin/bash
# One-command installer for the Telegram Restricted-Channel Downloader Bot.
# Usage (fresh Ubuntu/Debian server, as root):
#   curl -sSL https://raw.githubusercontent.com/nalascityboy-afk/telegram-downloader-bot/main/install.sh | sudo bash
set -e
APP_DIR="/opt/downloader-bot"
REPO="https://github.com/nalascityboy-afk/telegram-downloader-bot.git"

if [ "$(id -u)" -ne 0 ]; then echo "Run as root (sudo bash)"; exit 1; fi
echo "== [1/7] packages =="
apt-get update -qq
apt-get install -y -qq python3 python3-venv git curl sqlite3 cron > /dev/null
echo "== [2/7] code =="
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull -q
else
  mkdir -p "$APP_DIR"
  if [ -n "$LOCAL_SRC" ] && [ -d "$LOCAL_SRC" ]; then
    cp -r "$LOCAL_SRC"/. "$APP_DIR"/
  else
    git clone -q "$REPO" "$APP_DIR.tmp" && cp -r "$APP_DIR.tmp"/. "$APP_DIR"/ && rm -rf "$APP_DIR.tmp"
  fi
fi
cd "$APP_DIR"
echo "== [3/7] venv =="
[ -d venv ] || python3 -m venv venv
venv/bin/pip install -q --upgrade pip
venv/bin/pip install -q -r requirements.txt
echo "== [4/7] config =="
prompt_secret() { # $1=var $2=label
  local cur=""; [ -f .env ] && cur=$(grep -E "^$1=" .env | cut -d= -f2-)
  if [ -n "$cur" ]; then echo "$2: (kept existing)"; eval "$1=\"\$cur\""; return; fi
  read -rsp "$2: " val; echo
  [ -z "$val" ] && { echo "empty — abort"; exit 1; }
  eval "$1=\"\$val\""
}
prompt_plain() { # $1=var $2=label $3=default
  local cur=""; [ -f .env ] && cur=$(grep -E "^$1=" .env | cut -d= -f2-)
  if [ -n "$cur" ]; then echo "$2: (kept existing)"; eval "$1=\"\$cur\""; return; fi
  read -rp "$2 [$3]: " val; val=${val:-$3}
  eval "$1=\"\$val\""
}
prompt_secret RESTRICTED_BOT_TOKEN "Bot token (from @BotFather)"
prompt_plain TG_API_ID "API ID (my.telegram.org)" ""
prompt_secret TG_API_HASH "API HASH (my.telegram.org)"
prompt_plain BOT_OWNER_ID "Owner numeric Telegram ID (/myid in any bot)" ""
cat > .env <<EOF
RESTRICTED_BOT_TOKEN=$RESTRICTED_BOT_TOKEN
TG_API_ID=$TG_API_ID
TG_API_HASH=$TG_API_HASH
BOT_OWNER_ID=$BOT_OWNER_ID
DATA_DIR=$APP_DIR/data
EOF
chmod 600 .env
chmod +x run_bot.sh check_bot.sh
echo "== [5/7] verify config =="
DATA_DIR="$APP_DIR/data" ./venv/bin/python bot.py --check
echo "== [6/7] service =="
cat > /etc/systemd/system/downloader-bot.service <<EOF
[Unit]
Description=Telegram Restricted-Channel Downloader Bot
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/bot.py
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable -q downloader-bot
systemctl restart downloader-bot
sleep 4
echo "== [7/7] watchdog cron =="
CRON="*/5 * * * * bash $APP_DIR/check_bot.sh >> $APP_DIR/watchdog.log 2>&1"
(crontab -l 2>/dev/null | grep -v "check_bot.sh"; echo "$CRON") | crontab -
echo
echo "----- STATUS -----"
systemctl is-active downloader-bot
tail -n 5 "$APP_DIR"/bot.log 2>/dev/null || true
echo
echo "Done! Open your bot in Telegram and press /start, then pick a language."
echo "Connect your Telegram account with /login (QR or code) to download from private chats."

# Telegram Restricted-Channel Downloader Bot 📥

> 🇮🇷 [راهنمای فارسی](README_FA.md)

A Telegram bot that downloads media from **private/restricted** channels and groups.
Bots can't read forward-restricted content, so this project pairs a Bot API bot
(access control, menus, re-uploads) with a Telethon **userbot** (your own Telegram
account) that does the actual downloading.

**Trilingual:** 🇮🇷 فارسی · 🇬🇧 English · ☀️ کوردی — pick at `/start`, change anytime
with the 🌐 button or `/lang`.

## Features

- 📷 Photos, 🎬 videos, 📁 files, 📝 plain text via message links:
  `https://t.me/channel/123` and `https://t.me/c/123456/789`
- 🔗 Invite links (`t.me/+hash`): joins the account, then you send the message link
- 🔑 Per-user login: QR scan **or** login code (code typed in *words*, never digits)
  + 2FA password support
- 👑 Admin panel: add/remove users, promote/demote admins, connected accounts,
  full ownership transfer
- 🆘 Support desk: tickets + live chat with reply routing
- 📦 Files over ~48 MB are sent directly by the userbot (Bot API cap bypass)
- 🔄 systemd service + cron watchdog + crash-loop runner

## 1-command install (fresh Ubuntu/Debian server, as root)

```bash
curl -sSL https://raw.githubusercontent.com/nalascityboy-afk/telegram-downloader-bot/main/install.sh | sudo bash
```

The installer asks for 4 things (nothing secret is stored in git):

| Prompt | Where to get it |
|---|---|
| Bot token | [@BotFather](https://t.me/BotFather) → `/newbot` |
| API ID / API HASH | [my.telegram.org](https://my.telegram.org) → API development tools |
| Owner numeric ID | send `/myid` to any bot, or check with [@userinfobot](https://t.me/userinfobot) |

It then verifies config (`bot.py --check`), enables the systemd service and a
5-minute watchdog cron. Open your bot, press **/start**, pick a language, then
**/login** to connect your Telegram account (Settings → Devices → Link Desktop
Device for QR).

## Manual install

```bash
git clone https://github.com/nalascityboy-afk/telegram-downloader-bot.git
cd telegram-downloader-bot
python3 -m venv venv && ./venv/bin/python -m pip install -r requirements.txt
cp .env.example .env   # then edit .env
./venv/bin/python bot.py --check   # must print "config OK"
nohup bash run_bot.sh >/dev/null 2>&1 &
# watchdog (optional): */5 * * * * bash /path/to/check_bot.sh
```

Config lives in `.env` (see `.env.example`). Required vars:

- `RESTRICTED_BOT_TOKEN`, `TG_API_ID`, `TG_API_HASH`, `BOT_OWNER_ID`
- Optional: `DATA_DIR` (default `./data`), `DL_DIR` (default `<DATA_DIR>/downloads`)

## Usage

1. `/start` → choose language → help + button menu appears.
2. `/login` → QR or code → your account connects.
   (Private chats work only if **you** or the operator account is a member.
   Send an invite link first if the account must join.)
3. Send a message link → bot downloads and re-sends the media to you.
4. `/logout` disconnects your account. `/support` opens tickets/live chat.

Admin commands: `/admin` panel, `/adduser`, `/deluser`, `/promote`, `/demote`,
`/transfer`, `/users`, `/tickets`, `/accounts`, `/lang`.

## Updating

```bash
cd /opt/downloader-bot && git pull && ./venv/bin/pip install -r requirements.txt \
  && sudo systemctl restart downloader-bot
```

## Troubleshooting

- `Missing required env var` → `.env` is incomplete; re-run installer or edit `.env`.
- `userbot NOT authorized` in logs → press `/login` in the bot and connect again.
- `NOTMEMBER` / "not a member of this private chat" → connect a member account
  via `/login`, or send the invite link so the operator account can join.
- `PhoneCodeExpiredError` → codes live ~2 min; the bot auto-resends once, then
  use `/login` again.
- Heavy files arrive "directly" from the user account — that's the >48 MB path,
  not a bug.
- `database is locked` → two processes share one `.session`; keep a single
  instance (systemd already does).

## Security notes

- Never commit `.env` or `*.session` files — `.gitignore` already excludes them.
- Login codes must be typed as **words** inside Telegram (digits get rejected by
  Telegram itself for the account being logged into).
- If a token/session leaks: revoke via [@BotFather](https://t.me/BotFather)
  (`/revoke`) and terminate sessions in Telegram → Settings → Devices.

## Layout

- `bot.py` — bot + userbot logic (env config, polling, handlers)
- `lang.py` — fa/en/ckb strings (missing key falls back to Persian)
- `run_bot.sh` — crash-loop runner · `check_bot.sh` — cron watchdog
- `install.sh` — one-command server setup · `requirements.txt`

MIT licensed — see [LICENSE](LICENSE).

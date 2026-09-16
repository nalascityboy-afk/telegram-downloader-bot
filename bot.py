#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restricted channel/group downloader bot (Bot API + Telethon userbot).
Trilingual (fa/en/ckb). Config via environment variables only — no secrets in code.
"""
import asyncio
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from lang import LANGS, DEFAULT as DEFAULT_LANG, LANG_NAMES, get as _get

# ── CONFIG (env only) ──
def req_env(name):
    v = (os.environ.get(name) or "").strip()
    if not v:
        raise SystemExit(f"Missing required env var: {name} (see .env.example)")
    return v


BOT_TOKEN = req_env("RESTRICTED_BOT_TOKEN")
API_ID = int(req_env("TG_API_ID"))
API_HASH = req_env("TG_API_HASH")
OWNER_ID_FALLBACK = int(os.environ.get("BOT_OWNER_ID", "0") or 0)

DATA_DIR = Path(os.environ.get("DATA_DIR") or (Path(__file__).parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "restricted_bot_users.json"
LANGS_FILE = DATA_DIR / "langs.json"
TICKETS_FILE = DATA_DIR / "support_tickets.json"
SESSION = str(DATA_DIR / "userbot_session")
SESSIONS_DIR = DATA_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)
DL_DIR = Path(os.environ.get("DL_DIR") or (DATA_DIR / "downloads"))
DL_DIR.mkdir(parents=True, exist_ok=True)

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("rbot")

# ── I18N ──
def load_langs():
    try:
        if LANGS_FILE.exists():
            d = json.loads(LANGS_FILE.read_text())
            return {int(k): v for k, v in d.items() if v in LANGS}
    except Exception as e:
        log.warning("langs load fail: %s", e)
    return {}


def save_langs():
    try:
        LANGS_FILE.write_text(json.dumps({str(k): v for k, v in user_langs.items()}, ensure_ascii=False))
    except Exception as e:
        log.warning("langs save fail: %s", e)


user_langs = load_langs()


def get_lang(uid):
    return user_langs.get(uid, DEFAULT_LANG)


def set_lang(uid, code):
    user_langs[uid] = code
    save_langs()


def t(lang_or_uid, key, **kw):
    lang = lang_or_uid if isinstance(lang_or_uid, str) else get_lang(lang_or_uid)
    tpl = _get(lang, key)
    try:
        return tpl.format(**kw) if kw else tpl
    except Exception:
        return tpl


# ── STORAGE ──
def load_db():
    try:
        if USERS_FILE.exists():
            d = json.loads(USERS_FILE.read_text())
            owner = int(d.get("owner") or OWNER_ID_FALLBACK or 0)
            return owner, set(d.get("admins", [owner])), set(d.get("users", [owner]))
    except Exception as e:
        log.warning("db load fail: %s", e)
    return OWNER_ID_FALLBACK, {OWNER_ID_FALLBACK}, {OWNER_ID_FALLBACK}


def save_db(admins, users):
    USERS_FILE.write_text(json.dumps({"owner": owner_id, "admins": sorted(admins), "users": sorted(users)}, ensure_ascii=False))


owner_id, admins, users = load_db()
if owner_id:
    admins.add(owner_id)
    users.add(owner_id)
    save_db(admins, users)


def is_admin(uid):
    return uid in admins


def is_allowed(uid):
    return uid in users or uid in admins


# ── BOT HTTP ──
import requests
_session = requests.Session()


def api_call(method, data=None, files=None, timeout=120):
    for attempt in range(3):
        try:
            r = _session.post(f"{API}/{method}", data=data, files=files, timeout=timeout)
            j = r.json()
            if j.get("ok"):
                return j["result"]
            if j.get("parameters", {}).get("retry_after"):
                time.sleep(j["parameters"]["retry_after"] + 1)
                continue
            raise RuntimeError(j.get("description", str(j)))
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)
    raise RuntimeError("api failed")


def send_msg(chat_id, text, parse="HTML"):
    try:
        api_call("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": parse,
                                 "disable_web_page_preview": True})
    except Exception as e:
        log.warning("send fail: %s", e)


def send_file_bot(chat_id, path: Path, caption="", kind="doc"):
    size = path.stat().st_size
    if size > 48 * 1024 * 1024:
        return None  # too big → send via userbot
    method = {"photo": "sendPhoto", "video": "sendVideo"}.get(kind, "sendDocument")
    field = {"photo": "photo", "video": "video"}.get(kind, "document")
    with open(path, "rb") as f:
        api_call(method, {"chat_id": chat_id, "caption": caption[:1000]},
                 files={field: (path.name, f)}, timeout=300)
    return True


# ── KEYBOARDS ──
ACTIONS = ["login", "logout", "myid", "help", "admin", "menu", "support", "lang"]
ACTION_BY_LABEL = {}
for _l in LANGS:
    for _a in ACTIONS:
        ACTION_BY_LABEL[_get(_l, "btn_" + _a)] = _a


def _kb(obj):
    return json.dumps(obj, ensure_ascii=False)


def lang_kb():
    return _kb({"inline_keyboard": [
        [{"text": LANG_NAMES[c], "callback_data": f"lang:set:{c}"} for c in LANGS],
    ]})


def admin_kb(L):
    return _kb({"inline_keyboard": [
        [{"text": t(L, "adm_add"), "callback_data": "adm:add"},
         {"text": t(L, "adm_del"), "callback_data": "adm:del"}],
        [{"text": t(L, "adm_list"), "callback_data": "adm:list"}],
        [{"text": t(L, "adm_promote"), "callback_data": "adm:promote"},
         {"text": t(L, "adm_demote"), "callback_data": "adm:demote"}],
        [{"text": t(L, "adm_accounts"), "callback_data": "adm:accounts"}],
        [{"text": t(L, "adm_transfer"), "callback_data": "adm:transfer"}],
    ]})


def confirm_transfer_kb(target, L):
    return _kb({"inline_keyboard": [
        [{"text": t(L, "transfer_yes"), "callback_data": f"adm:transfer_yes:{target}"},
         {"text": t(L, "transfer_no"), "callback_data": "adm:transfer_no"}],
    ]})


def login_choice_kb(L):
    return _kb({"inline_keyboard": [
        [{"text": t(L, "qr_btn"), "callback_data": "login:qr"},
         {"text": t(L, "code_btn"), "callback_data": "login:code"}],
    ]})


def support_kb(L):
    return _kb({"inline_keyboard": [
        [{"text": t(L, "sup_ticket"), "callback_data": "sup:new_ticket"},
         {"text": t(L, "sup_chat"), "callback_data": "sup:new_chat"}],
    ]})


def ticket_kb(nid, L):
    # labels stay short; per-admin language applied where we know admin
    return _kb({"inline_keyboard": [
        [{"text": t(L, "ticket_reply"), "callback_data": f"sup:reply:{nid}"},
         {"text": t(L, "ticket_close"), "callback_data": f"sup:close:{nid}"}],
    ]})


def main_kb(L, admin):
    kb = [[{"text": t(L, "btn_login")}, {"text": t(L, "btn_logout")}],
          [{"text": t(L, "btn_myid")}, {"text": t(L, "btn_help")}],
          [{"text": t(L, "btn_support")}, {"text": t(L, "btn_lang")}]]
    if admin:
        kb.append([{"text": t(L, "btn_admin")}])
    return _kb({"keyboard": kb, "resize_keyboard": True})


# ── PANELS ──
pending = {}  # admin_id -> action


def show_lang_picker(chat_id, L):
    try:
        api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "lang_pick"),
                                 "reply_markup": lang_kb()})
    except Exception as e:
        log.warning("lang picker fail: %s", e)


def show_panel(chat_id, L):
    try:
        api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "admin_panel"),
                                 "parse_mode": "HTML", "reply_markup": admin_kb(L)})
    except Exception as e:
        log.warning("panel fail: %s", e)


def send_menu(chat_id, uid):
    L = get_lang(uid)
    try:
        api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "menu_title"),
                                 "reply_markup": main_kb(L, is_admin(uid))})
    except Exception as e:
        log.warning("menu fail: %s", e)


def show_support(chat_id, L):
    try:
        api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "sup_title"),
                                 "parse_mode": "HTML", "reply_markup": support_kb(L)})
    except Exception as e:
        log.warning("support panel fail: %s", e)


async def build_accounts_text(L):
    import glob as _g
    lines = []
    if client_ready:
        try:
            me = await client.get_me()
            nm = f"{getattr(me, 'first_name', '')} (@{getattr(me, 'username', t(L, 'accounts_user_q'))})"
            lines.append(t(L, "accounts_main", nm=nm))
        except Exception:
            lines.append(t(L, "accounts_main_ok"))
    for f in sorted(_g.glob(str(SESSIONS_DIR / "*.session"))):
        try:
            auid = int(Path(f).stem)
        except ValueError:
            continue
        nm = t(L, "accounts_user_q")
        c = await get_user_client(auid)
        if c is not None:
            try:
                me = await c.get_me()
                nm = f"{getattr(me, 'first_name', '')} (@{getattr(me, 'username', t(L, 'accounts_user_q'))})"
            except Exception:
                nm = t(L, "accounts_user_ok")
        lines.append(f"• <code>{auid}</code>: {nm}")
    return t(L, "accounts_title") + "\n".join(lines) if lines else t(L, "accounts_none")


async def handle_callback(cb):
    global owner_id
    uid = (cb.get("from") or {}).get("id")
    msg = cb.get("message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    mid = msg.get("message_id")
    data = cb.get("data", "")
    if not uid or not chat_id:
        return
    L = get_lang(uid)
    if data.startswith("lang:set:"):
        code = data.split(":")[2]
        if code not in LANGS:
            return
        try:
            api_call("answerCallbackQuery", {"callback_query_id": cb["id"]})
        except Exception:
            pass
        set_lang(uid, code)
        L = code
        role = t(L, "role_admin") if is_admin(uid) else t(L, "role_user")
        try:
            api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                         "text": t(L, "lang_set_ok")})
        except Exception:
            pass
        send_msg(chat_id, t(L, "hello", role=role, help=t(L, "help_text")))
        send_menu(chat_id, uid)
        if is_admin(uid):
            show_panel(chat_id, L)
        return
    try:
        api_call("answerCallbackQuery", {"callback_query_id": cb["id"]})
    except Exception:
        pass
    if data == "login:qr" or data == "login:code":
        if not is_allowed(uid):
            return
        if data == "login:qr":
            try:
                api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                             "text": t(L, "login_qr_chosen")})
            except Exception:
                pass
            start_qr_login(chat_id, uid)
        else:
            login_code_state[uid] = {"step": "phone", "ts": time.time()}
            try:
                api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                             "text": t(L, "login_phone_ask"),
                                             "parse_mode": "HTML"})
            except Exception:
                send_msg(chat_id, t(L, "login_phone_ask_simple"))
        return
    if data in ("sup:new_ticket", "sup:new_chat"):
        if not is_allowed(uid):
            return
        if data == "sup:new_ticket":
            support_state[uid] = {"mode": "await_ticket"}
            try:
                api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                             "text": t(L, "sup_ticket_ask")})
            except Exception:
                send_msg(chat_id, t(L, "sup_ticket_ask_simple"))
        else:
            active_chats[uid] = {"ts": time.time()}
            try:
                api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                             "text": t(L, "sup_chat_ok")})
            except Exception:
                send_msg(chat_id, t(L, "sup_chat_ok_simple"))
            for a in sorted(admins):
                if a != uid:
                    try:
                        send_msg(a, t(get_lang(a), "sup_chat_admin", uid=uid))
                    except Exception:
                        pass
        return
    if data.startswith("sup:reply:") or data.startswith("sup:close:"):
        if not is_admin(uid):
            return
        try:
            nid = int(data.split(":")[2])
        except ValueError:
            return
        tickets = load_tickets()
        t_ = next((x for x in tickets if x["id"] == nid), None)
        if t_ is None:
            return
        if data.startswith("sup:reply:"):
            admin_ticket_reply[uid] = nid
            send_msg(chat_id, t(L, "ticket_reply_ask", nid=nid))
        else:
            t_["status"] = "closed"
            save_tickets(tickets)
            api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                         "text": t(L, "ticket_closed", nid=nid)})
            try:
                send_msg(t_["user"], t(get_lang(t_["user"]), "ticket_closed_user", nid=nid))
            except Exception:
                pass
        return
    if not is_admin(uid):
        return
    if data == "adm:list":
        lst = "\n".join(f"• <code>{x}</code>" + (" 👑" if x in admins else "")
                        for x in sorted(users)) or t(L, "users_empty")
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "users_title", n=len(users), lst=lst),
                                     "parse_mode": "HTML", "reply_markup": admin_kb(L)})
    elif data == "adm:add":
        pending[uid] = "add"
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "adm_add_ask"),
                                     "reply_markup": admin_kb(L)})
    elif data == "adm:del":
        pending[uid] = "del"
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "adm_del_ask"),
                                     "reply_markup": admin_kb(L)})
    elif data == "adm:accounts":
        txt = await build_accounts_text(L)
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": txt,
                                     "parse_mode": "HTML", "reply_markup": admin_kb(L)})
    elif data == "adm:promote":
        pending[uid] = "promote"
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "adm_promote_ask"),
                                     "reply_markup": admin_kb(L)})
    elif data == "adm:demote":
        pending[uid] = "demote"
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "adm_demote_ask"),
                                     "reply_markup": admin_kb(L)})
    elif data == "adm:transfer":
        if uid != owner_id:
            try:
                api_call("answerCallbackQuery", {"callback_query_id": cb["id"], "text": t(L, "only_owner")})
            except Exception:
                pass
            return
        pending[uid] = "transfer"
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "transfer_ask"),
                                     "parse_mode": "HTML", "reply_markup": admin_kb(L)})
    elif data.startswith("adm:transfer_yes:"):
        if uid != owner_id:
            return
        try:
            new_owner = int(data.split(":")[2])
        except ValueError:
            return
        admins.add(new_owner)
        users.add(new_owner)
        owner_id = new_owner
        save_db(admins, users)
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "transfer_done", target=new_owner),
                                     "parse_mode": "HTML"})
        try:
            send_msg(new_owner, t(get_lang(new_owner), "transfer_new"))
        except Exception:
            pass
    elif data == "adm:transfer_no":
        api_call("editMessageText", {"chat_id": chat_id, "message_id": mid,
                                     "text": t(L, "transfer_cancelled")})


# ── TELETHON ──
client = None
client_ready = False


async def init_userbot():
    global client, client_ready
    from telethon import TelegramClient
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    if await client.is_user_authorized():
        me = await client.get_me()
        log.info("userbot OK: %s (%s)", me.id, getattr(me, "first_name", ""))
        client_ready = True
    else:
        log.warning("userbot NOT authorized — needs login (phone+code)")
        client_ready = False
    return client


# ── MULTI-ACCOUNT ──
user_clients = {}   # tg_user_id -> TelegramClient
login_tasks = {}    # tg_user_id -> asyncio.Task


def session_path(uid):
    return str(SESSIONS_DIR / str(uid))


async def get_user_client(uid):
    c = user_clients.get(uid)
    if c is not None:
        try:
            if c.is_connected():
                return c
        except Exception:
            pass
    import os as _os
    if not _os.path.exists(session_path(uid) + ".session"):
        return None
    from telethon import TelegramClient as _TC
    c = _TC(session_path(uid), API_ID, API_HASH)
    try:
        await c.connect()
        if await c.is_user_authorized():
            user_clients[uid] = c
            return c
        await c.disconnect()
    except Exception as e:
        log.warning("user session %s fail: %s", uid, e)
    return None


async def clients_for(uid):
    out = []
    uc = await get_user_client(uid)
    if uc is not None:
        out.append(uc)
    if client_ready and client is not None and (not out or out[0] is not client):
        out.append(client)
    return out


def make_qr_png(url, out):
    import qrcode
    qrcode.make(url).save(out)


async def qr_login_flow(chat_id, uid):
    L = get_lang(uid)
    from telethon import TelegramClient as _TC
    old = user_clients.pop(uid, None)
    if old is not None:
        try:
            await old.disconnect()
        except Exception:
            pass
    for suf in (".session", ".session-journal"):
        try:
            (SESSIONS_DIR / f"{uid}{suf}").unlink(missing_ok=True)
        except Exception:
            pass
    c = _TC(session_path(uid), API_ID, API_HASH)
    try:
        await c.connect()
        qr = await c.qr_login()
    except Exception as e:
        send_msg(chat_id, t(L, "login_start_fail", e=e))
        try:
            await c.disconnect()
        except Exception:
            pass
        login_tasks.pop(uid, None)
        return
    import datetime as _dt
    qr_msg_id = None
    user = None
    for rnd in range(1, 5):
        try:
            await qr.recreate()
        except Exception as e:
            send_msg(chat_id, t(L, "login_start_fail", e=e))
            break
        png = DL_DIR / f"qr_{uid}_{rnd}.png"
        try:
            await asyncio.get_running_loop().run_in_executor(None, make_qr_png, qr.url, str(png))
            if qr_msg_id is not None:
                try:
                    api_call("deleteMessage", {"chat_id": chat_id, "message_id": qr_msg_id})
                except Exception:
                    pass
            with open(png, "rb") as f:
                sent = api_call("sendPhoto", {"chat_id": chat_id, "caption": t(L, "qr_caption")},
                                files={"photo": ("qr.png", f)}, timeout=60)
            qr_msg_id = sent["message_id"]
        except Exception as e:
            send_msg(chat_id, t(L, "qr_send_fail", e=e))
            break
        finally:
            try:
                png.unlink()
            except Exception:
                pass
        try:
            wait_s = (qr.expires - _dt.datetime.now(tz=_dt.timezone.utc)).total_seconds() - 2
            if wait_s < 5:
                continue
            user = await asyncio.wait_for(qr.wait(), timeout=wait_s)
            break
        except asyncio.TimeoutError:
            continue
        except Exception as e:
            send_msg(chat_id, t(L, "login_fail", e=e))
            break
    if user is None:
        try:
            if qr_msg_id is not None:
                api_call("deleteMessage", {"chat_id": chat_id, "message_id": qr_msg_id})
        except Exception:
            pass
        try:
            await c.disconnect()
        except Exception:
            pass
        for suf in (".session", ".session-journal"):
            try:
                (SESSIONS_DIR / f"{uid}{suf}").unlink(missing_ok=True)
            except Exception:
                pass
        login_tasks.pop(uid, None)
        send_msg(chat_id, t(L, "qr_timeout"))
        return
    user_clients[uid] = c
    login_tasks.pop(uid, None)
    try:
        me = await c.get_me()
        nm = getattr(me, "first_name", "") or ""
        send_msg(chat_id, t(L, "login_ok_groups", nm=nm))
    except Exception:
        send_msg(chat_id, t(L, "login_ok"))


# ── LOGIN WITH CODE ──
login_code_state = {}  # uid -> {step, phone, hash, ts, resent, client}

FA_NUM_WORDS = {
    "صفر": "0", "سفر": "0", "zero": "0",
    "یک": "1", "يک": "1", "یەک": "1", "یەك": "1", "one": "1",
    "دو": "2", "دوو": "2", "two": "2",
    "سه": "3", "سێ": "3", "three": "3",
    "چهار": "4", "چار": "4", "چوار": "4", "four": "4",
    "پنج": "5", "پێنج": "5", "پینج": "5", "five": "5",
    "شش": "6", "شیش": "6", "شەش": "6", "six": "6",
    "هفت": "7", "هەفت": "7", "حەوت": "7", "seven": "7",
    "هشت": "8", "هەشت": "8", "eight": "8",
    "نه": "9", "نۆ": "9", "nine": "9",
}
FA_DIG = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def normalize_code(text):
    t_ = text.translate(FA_DIG).replace("ي", "ی").replace("ك", "ک").lower()
    out = [FA_NUM_WORDS[w] for w in re.findall(r"[a-z\u0600-\u06FF]+", t_) if w in FA_NUM_WORDS]
    out.extend(re.findall(r"\d", t_))
    return "".join(out)


def start_qr_login(chat_id, uid):
    L = get_lang(uid)
    t_ = login_tasks.get(uid)
    if t_ is not None and not t_.done():
        send_msg(chat_id, t(L, "login_in_progress"))
        return
    send_msg(chat_id, t(L, "login_qr_making"))
    login_tasks[uid] = asyncio.create_task(qr_login_flow(chat_id, uid))


async def drop_code_login(uid):
    st = login_code_state.pop(uid, None) or {}
    c = st.get("client")
    if c is not None:
        try:
            await c.disconnect()
        except Exception:
            pass
    for suf in (".session", ".session-journal"):
        try:
            (SESSIONS_DIR / f"{uid}{suf}").unlink(missing_ok=True)
        except Exception:
            pass


async def finish_code_login(chat_id, uid, st):
    L = get_lang(uid)
    c = st.get("client")
    login_code_state.pop(uid, None)
    if c is None:
        send_msg(chat_id, t(L, "login_problem"))
        return
    user_clients[uid] = c
    try:
        me = await c.get_me()
        nm = getattr(me, "first_name", "") or ""
        send_msg(chat_id, t(L, "login_ok_groups", nm=nm))
    except Exception:
        send_msg(chat_id, t(L, "login_ok"))


async def login_step_phone(chat_id, uid, text, st):
    L = get_lang(uid)
    ph = re.sub(r"[^\d+]", "", text)
    if not re.fullmatch(r"\+\d{7,15}", ph):
        send_msg(chat_id, t(L, "phone_invalid"))
        return
    send_msg(chat_id, t(L, "login_sending_code"))
    from telethon import TelegramClient as _TC
    old = user_clients.pop(uid, None)
    if old is not None:
        try:
            await old.disconnect()
        except Exception:
            pass
    for suf in (".session", ".session-journal"):
        try:
            (SESSIONS_DIR / f"{uid}{suf}").unlink(missing_ok=True)
        except Exception:
            pass
    c = _TC(session_path(uid), API_ID, API_HASH)
    try:
        await c.connect()
        r = await c.send_code_request(ph)
    except Exception as e:
        try:
            await c.disconnect()
        except Exception:
            pass
        s = str(e)
        if "WAIT" in s.upper() or "FLOOD" in s.upper():
            send_msg(chat_id, t(L, "login_flood", e=e))
        else:
            send_msg(chat_id, t(L, "login_phone_fail", e=e))
        return
    st.update(step="code", phone=ph, hash=r.phone_code_hash, ts=time.time(), resent=False, client=c)
    send_msg(chat_id, t(L, "code_sent"))


async def login_step_code(chat_id, uid, text, st):
    L = get_lang(uid)
    code = normalize_code(text)
    if len(code) < 5:
        send_msg(chat_id, t(L, "code_unknown"))
        return
    c = st.get("client")
    if c is None:
        login_code_state.pop(uid, None)
        send_msg(chat_id, t(L, "login_problem"))
        return
    try:
        await c.sign_in(st["phone"], code, phone_code_hash=st["hash"])
    except Exception as e:
        name = type(e).__name__
        if name == "SessionPasswordNeededError":
            st["step"] = "password"
            st["ts"] = time.time()
            send_msg(chat_id, t(L, "pwd_need"))
            return
        if name == "PhoneCodeExpiredError":
            if not st.get("resent"):
                try:
                    r = await c.send_code_request(st["phone"])
                    st["hash"] = r.phone_code_hash
                    st["resent"] = True
                    st["ts"] = time.time()
                    send_msg(chat_id, t(L, "code_expired_new"))
                except Exception as e2:
                    send_msg(chat_id, t(L, "code_resend_fail", e=e2))
            else:
                await drop_code_login(uid)
                send_msg(chat_id, t(L, "code_expired"))
            return
        if name == "PhoneCodeInvalidError":
            send_msg(chat_id, t(L, "code_invalid"))
            return
        send_msg(chat_id, t(L, "login_fail", e=e))
        return
    await finish_code_login(chat_id, uid, st)


async def login_step_password(chat_id, uid, text, st):
    L = get_lang(uid)
    c = st.get("client")
    if c is None:
        login_code_state.pop(uid, None)
        send_msg(chat_id, t(L, "login_problem"))
        return
    try:
        await c.sign_in(password=text.strip())
    except Exception as e:
        if "Invalid" in type(e).__name__ or "invalid" in str(e).lower():
            send_msg(chat_id, t(L, "pwd_wrong"))
            return
        send_msg(chat_id, t(L, "login_fail", e=e))
        return
    await finish_code_login(chat_id, uid, st)


# ── SUPPORT (tickets + live chat) ──
support_state = {}       # uid -> {"mode": "await_ticket"}
active_chats = {}        # uid -> {"ts": ...}
admin_ticket_reply = {}  # admin_id -> ticket_id
fwd_map = {}             # (admin_chat_id, msg_id) -> user_id
CHAT_TTL = 1800
_NUM = r"(?:<code>)?(\d{5,})(?:</code>)?"
_B = r"(?:</b>)?"
CHAT_PATTERNS = [
    rf"چت زنده{_B} از {_NUM}", rf"کاربر {_NUM} چت زنده خواست",
    rf"Live chat{_B} from {_NUM}", rf"User {_NUM} requested live chat",
    rf"چاتی زیندوو{_B} لە {_NUM}", rf"بەکارهێنەر {_NUM} چاتی زیندووی داواکرد",
]


def find_chat_uid(rtext):
    for p in CHAT_PATTERNS:
        mt = re.search(p, rtext)
        if mt:
            return int(mt.group(1))
    return None


def load_tickets():
    try:
        if TICKETS_FILE.exists():
            return json.loads(TICKETS_FILE.read_text())
    except Exception as e:
        log.warning("tickets load fail: %s", e)
    return []


def save_tickets(tickets):
    TICKETS_FILE.write_text(json.dumps(tickets, ensure_ascii=False))


def parse_link(url: str):
    """-> dict(kind=msg|invite|unknown, ...)"""
    url = url.strip().split("?")[0].rstrip("/")
    m = re.search(r"t\.me/(\+[\w-]+|joinchat/[\w-]+)", url)
    if m:
        return {"kind": "invite", "hash": m.group(1).replace("joinchat/", "").lstrip("+")}
    m = re.search(r"t\.me/c/(\d+)/(\d+)", url)
    if m:
        return {"kind": "msg", "chat": int("-100" + m.group(1)), "msg_id": int(m.group(2))}
    m = re.search(r"t\.me/([A-Za-z0-9_]{4,})/(\d+)", url)
    if m:
        return {"kind": "msg", "chat": m.group(1), "msg_id": int(m.group(2))}
    return {"kind": "unknown"}


async def fetch_message(chat, msg_id, cl, L):
    from telethon.tl.functions.channels import JoinChannelRequest
    try:
        entity = await cl.get_entity(chat)
    except Exception:
        if isinstance(chat, str):
            try:
                await cl(JoinChannelRequest(chat))
                entity = await cl.get_entity(chat)
            except Exception as e:
                raise RuntimeError(t(L, "fetch_join_fail", e=e))
        else:
            raise RuntimeError("NOTMEMBER")
    msgs = await cl.get_messages(entity, ids=msg_id)
    msg = msgs if not isinstance(msgs, list) else (msgs[0] if msgs else None)
    if not msg:
        raise RuntimeError(t(L, "msg_not_found"))
    return entity, msg


async def download_msg_media(msg, msg_id, cl, L):
    if not msg.media and not msg.text:
        raise RuntimeError(t(L, "msg_empty"))
    if not msg.media:
        return None, msg.text or "", "text"
    path = await cl.download_media(msg, file=str(DL_DIR / f"{msg_id}_"))
    if not path:
        raise RuntimeError(t(L, "dl_fail"))
    p = Path(path)
    suf = p.suffix.lower()
    if suf in (".jpg", ".jpeg", ".png", ".webp"):
        kind = "photo"
    elif suf in (".mp4", ".mkv", ".mov", ".webm"):
        kind = "video"
    else:
        kind = "doc"
    return p, (msg.text or ""), kind


async def handle_link(chat_id, uid, url):
    L = get_lang(uid)
    info = parse_link(url)
    cls = await clients_for(uid)
    if info["kind"] == "invite":
        if not cls:
            send_msg(chat_id, t(L, "no_account_first"))
            return
        prog = api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "joining")})
        prog_id = prog["message_id"]
        last = None
        for cl in cls:
            try:
                from telethon.tl.functions.messages import ImportChatInviteRequest
                await cl(ImportChatInviteRequest(info["hash"]))
                api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                             "text": t(L, "joined_ok")})
                return
            except Exception as e:
                s = str(e)
                if "USER_ALREADY_PARTICIPANT" in s or "already" in s.lower():
                    api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                                 "text": t(L, "already_member")})
                    return
                if "INVITE_HASH_EXPIRED" in s or "INVITE_HASH_INVALID" in s:
                    api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                                 "text": t(L, "invite_bad")})
                    return
                last = e
                continue
        api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                     "text": t(L, "join_fail", e=last)})
        return
    if info["kind"] != "msg":
        send_msg(chat_id, t(L, "link_bad"))
        return
    if not cls:
        send_msg(chat_id, t(L, "no_account_qr"))
        return
    prog = api_call("sendMessage", {"chat_id": chat_id, "text": t(L, "downloading")})
    prog_id = prog["message_id"]
    last_err, not_member = None, False
    for cl in cls:
        try:
            entity, msg = await fetch_message(info["chat"], info["msg_id"], cl, L)
        except Exception as e:
            log.info("fetch fail uid=%s chat=%s msg=%s: %s %s", uid, info["chat"], info["msg_id"],
                     type(e).__name__, str(e)[:200])
            if str(e) == "NOTMEMBER":
                not_member = True
            last_err = e
            continue
        try:
            path, caption, kind = await download_msg_media(msg, info["msg_id"], cl, L)
            if path is None:  # text only
                api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                             "text": t(L, "text_msg", txt=caption[:4000])})
                return
            loop = asyncio.get_running_loop()
            sent = await loop.run_in_executor(None, send_file_bot, chat_id, path, caption, kind)
            if sent is None:
                await cl.send_file(uid, path, caption=caption[:1000])
                api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                             "text": t(L, "heavy_sent")})
            else:
                try:
                    api_call("deleteMessage", {"chat_id": chat_id, "message_id": prog_id})
                except Exception:
                    pass
            try:
                path.unlink()
            except Exception:
                pass
            return
        except Exception as e:
            last_err = e
            continue
    if not_member and str(last_err) == "NOTMEMBER":
        api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                     "text": t(L, "not_member")})
    else:
        try:
            api_call("editMessageText", {"chat_id": chat_id, "message_id": prog_id,
                                         "text": t(L, "err", e=last_err)})
        except Exception:
            send_msg(chat_id, t(L, "err", e=last_err))


# ── UPDATE LOOP ──
offset = 0


def get_updates():
    global offset
    r = _session.post(f"{API}/getUpdates", data={"offset": offset, "timeout": 40}, timeout=50)
    return r.json().get("result", [])


async def handle_update(u):
    if u.get("callback_query"):
        try:
            await handle_callback(u["callback_query"])
        except Exception as e:
            log.exception("callback err: %s", e)
        return
    m = u.get("message") or u.get("edited_message") or {}
    chat = m.get("chat", {})
    chat_id = chat.get("id")
    uid = (m.get("from") or {}).get("id")
    text = (m.get("text") or "").strip()
    if not chat_id or not uid:
        return
    if not is_allowed(uid):
        send_msg(chat_id, t(DEFAULT_LANG, "no_access", uid=uid))
        return
    L = get_lang(uid)
    if text in ACTION_BY_LABEL:
        act = ACTION_BY_LABEL[text]
        text = "/" + {"login": "login", "logout": "logout", "myid": "myid", "help": "help",
                       "admin": "admin", "menu": "menu", "support": "support", "lang": "lang"}[act]
    rep_msg = m.get("reply_to_message") or {}
    rep = rep_msg.get("message_id")
    if rep and (chat_id, rep) in fwd_map:
        target = fwd_map[(chat_id, rep)]
        try:
            send_msg(target, t(get_lang(target), "support_reply", text=text))
            send_msg(chat_id, t(L, "msg_delivered"))
        except Exception as e:
            send_msg(chat_id, t(L, "send_fail", e=e))
        return
    if rep and is_admin(uid):
        rtext = rep_msg.get("text", "") or ""
        target = find_chat_uid(rtext)
        if target:
            try:
                send_msg(target, t(get_lang(target), "support_reply", text=text))
                send_msg(chat_id, t(L, "msg_delivered"))
            except Exception as e:
                send_msg(chat_id, t(L, "send_fail", e=e))
            return
        send_msg(chat_id, t(L, "chat_reply_hint"))
        return
    ar = admin_ticket_reply.get(uid)
    if ar is not None and not text.startswith("/"):
        tickets = load_tickets()
        t_ = next((x for x in tickets if x["id"] == ar), None)
        if t_ is None:
            admin_ticket_reply.pop(uid, None)
            send_msg(chat_id, t(L, "ticket_not_found"))
            return
        t_["replies"].append({"by": uid, "text": text[:2000], "ts": int(time.time())})
        t_["status"] = "answered"
        save_tickets(tickets)
        admin_ticket_reply.pop(uid, None)
        try:
            send_msg(t_["user"], t(get_lang(t_["user"]), "ticket_user_reply", ar=ar, text=text[:2000]))
            send_msg(chat_id, t(L, "ticket_answered", ar=ar))
        except Exception as e:
            send_msg(chat_id, t(L, "send_fail", e=e))
        return
    sp = support_state.get(uid)
    if sp is not None and not text.startswith("/") and sp.get("mode") == "await_ticket":
        tickets = load_tickets()
        nid = (max([x["id"] for x in tickets]) + 1) if tickets else 1
        tickets.append({"id": nid, "user": uid, "text": text[:2000],
                        "ts": int(time.time()), "status": "open", "replies": []})
        save_tickets(tickets)
        support_state.pop(uid, None)
        send_msg(chat_id, t(L, "ticket_created", nid=nid))
        for a in sorted(admins):
            try:
                api_call("sendMessage", {"chat_id": a,
                                         "text": t(get_lang(a), "ticket_new", nid=nid, uid=uid, text=text[:1500]),
                                         "parse_mode": "HTML", "reply_markup": ticket_kb(nid, get_lang(a))})
            except Exception:
                pass
        return
    if uid in active_chats and not text.startswith("/"):
        ch = active_chats[uid]
        if time.time() - ch.get("ts", 0) > CHAT_TTL:
            active_chats.pop(uid, None)
            send_msg(chat_id, t(L, "chat_expired"))
            return
        if "t.me/" not in text:
            ch["ts"] = time.time()
            if len(fwd_map) > 500:
                for _ in range(100):
                    fwd_map.pop(next(iter(fwd_map)))
            for a in sorted(admins):
                if a != uid:
                    try:
                        s = api_call("sendMessage", {"chat_id": a,
                                                     "text": t(get_lang(a), "chat_live", uid=uid, text=text[:1500]),
                                                     "parse_mode": "HTML"})
                        fwd_map[(a, s["message_id"])] = uid
                    except Exception:
                        pass
            return
    st = login_code_state.get(uid)
    if st is not None and not text.startswith("/"):
        if time.time() - st.get("ts", 0) > 600:
            await drop_code_login(uid)
            send_msg(chat_id, t(L, "login_timeout"))
            return
        if st["step"] == "phone":
            await login_step_phone(chat_id, uid, text, st)
            return
        if st["step"] == "code":
            await login_step_code(chat_id, uid, text, st)
            return
        if st["step"] == "password":
            await login_step_password(chat_id, uid, text, st)
            return
    if uid in pending and not text.startswith("/"):
        action = pending.pop(uid)
        mt = re.fullmatch(r"\d+", text.strip())
        if not mt:
            send_msg(chat_id, t(L, "id_not_found"))
            if is_admin(uid):
                show_panel(chat_id, L)
            return
        target = int(mt.group())
        if action == "add":
            users.add(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "user_added", target=target))
            try:
                send_msg(target, t(get_lang(target), "user_added_msg"))
            except Exception:
                pass
        elif action == "promote":
            admins.add(target)
            users.add(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "user_promoted", target=target))
            try:
                send_msg(target, t(get_lang(target), "admin_promoted_msg"))
            except Exception:
                pass
        elif action == "demote":
            if target == owner_id:
                send_msg(chat_id, t(L, "owner_no_demote"))
                return
            if target == uid:
                send_msg(chat_id, t(L, "self_no_demote"))
                return
            if target not in admins:
                send_msg(chat_id, t(L, "not_admin"))
                return
            admins.discard(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "demoted", target=target))
        elif action == "transfer":
            if uid != owner_id:
                send_msg(chat_id, t(L, "owner_transfer_only"))
                return
            if target == uid:
                send_msg(chat_id, t(L, "already_owner"))
                return
            api_call("sendMessage", {"chat_id": chat_id,
                                     "text": t(L, "transfer_confirm", target=target),
                                     "parse_mode": "HTML",
                                     "reply_markup": confirm_transfer_kb(target, L)})
            return
        else:
            if target == owner_id:
                send_msg(chat_id, t(L, "owner_no_delete"))
                return
            users.discard(target)
            admins.discard(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "user_deleted", target=target))
        if is_admin(uid):
            show_panel(chat_id, L)
        return
    if text.startswith("/"):
        parts = text.split()
        cmd = parts[0].split("@")[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == "/start":
            if uid not in user_langs:
                show_lang_picker(chat_id, DEFAULT_LANG)
                return
            role = t(L, "role_admin") if is_admin(uid) else t(L, "role_user")
            send_msg(chat_id, t(L, "hello", role=role, help=t(L, "help_text")))
            send_menu(chat_id, uid)
            if is_admin(uid):
                show_panel(chat_id, L)
        elif cmd in ("/lang", "/language"):
            show_lang_picker(chat_id, L)
        elif cmd == "/menu":
            send_menu(chat_id, uid)
            if is_admin(uid):
                show_panel(chat_id, L)
        elif cmd in ("/admin", "/panel", "/manage"):
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            show_panel(chat_id, L)
        elif cmd == "/help":
            send_msg(chat_id, t(L, "help_text"))
        elif cmd == "/myid":
            send_msg(chat_id, t(L, "myid_is", uid=uid))
        elif cmd == "/login":
            uc = await get_user_client(uid)
            if uc is not None:
                try:
                    me = await uc.get_me()
                    nm = getattr(me, "first_name", "") or ""
                    send_msg(chat_id, t(L, "login_connected", nm=nm))
                except Exception:
                    send_msg(chat_id, t(L, "login_connected_simple"))
                return
            try:
                api_call("sendMessage", {"chat_id": chat_id,
                                         "text": t(L, "login_choose"),
                                         "reply_markup": login_choice_kb(L)})
            except Exception:
                send_msg(chat_id, "🔑 /login")
        elif cmd == "/support":
            show_support(chat_id, L)
        elif cmd == "/end":
            if uid in active_chats:
                active_chats.pop(uid, None)
                send_msg(chat_id, t(L, "chat_closed"))
                for a in sorted(admins):
                    if a != uid:
                        try:
                            send_msg(a, t(get_lang(a), "chat_closed_user", uid=uid))
                        except Exception:
                            pass
                return
            rep2msg = m.get("reply_to_message") or {}
            rep2 = rep2msg.get("message_id")
            target = None
            if rep2 and (chat_id, rep2) in fwd_map:
                target = fwd_map.pop((chat_id, rep2))
            elif rep2:
                rtext2 = rep2msg.get("text", "") or ""
                target = find_chat_uid(rtext2)
            if target:
                active_chats.pop(target, None)
                send_msg(chat_id, t(L, "chat_closed"))
                try:
                    send_msg(target, t(get_lang(target), "chat_closed_admin"))
                except Exception:
                    pass
                return
            send_msg(chat_id, t(L, "no_active_chat"))
        elif cmd == "/tickets":
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            tickets = [x for x in load_tickets() if x.get("status") != "closed"]
            if not tickets:
                send_msg(chat_id, t(L, "tickets_none"))
                return
            lines = [t(L, "ticket_line", nid=x['id'], st=x.get('status'), uid=x['user'], txt=x['text'][:80])
                     for x in sorted(tickets, key=lambda x: x["id"])]
            send_msg(chat_id, t(L, "tickets_open", lines="\n".join(lines)))
        elif cmd == "/cancel":
            t_ = login_tasks.pop(uid, None)
            if t_ is not None:
                t_.cancel()
            await drop_code_login(uid)
            send_msg(chat_id, t(L, "login_cancelled"))
        elif cmd == "/logout":
            t_ = login_tasks.pop(uid, None)
            if t_ is not None:
                t_.cancel()
            c = user_clients.pop(uid, None)
            if c is not None:
                try:
                    await c.disconnect()
                except Exception:
                    pass
            for suf in (".session", ".session-journal"):
                try:
                    (SESSIONS_DIR / f"{uid}{suf}").unlink(missing_ok=True)
                except Exception:
                    pass
            send_msg(chat_id, t(L, "logged_out"))
        elif cmd == "/accounts":
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            send_msg(chat_id, await build_accounts_text(L))
        elif cmd in ("/adduser", "/add"):
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            try:
                new_id = int(arg)
                users.add(new_id)
                save_db(admins, users)
                send_msg(chat_id, t(L, "user_added", target=new_id))
                try:
                    send_msg(new_id, t(get_lang(new_id), "user_added_msg"))
                except Exception:
                    pass
            except ValueError:
                send_msg(chat_id, t(L, "fmt_adduser"))
        elif cmd in ("/deluser", "/del", "/remove"):
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            try:
                rem = int(arg)
                if rem == owner_id:
                    send_msg(chat_id, t(L, "owner_no_delete"))
                    return
                users.discard(rem)
                admins.discard(rem)
                save_db(admins, users)
                send_msg(chat_id, t(L, "user_deleted", target=rem))
            except ValueError:
                send_msg(chat_id, t(L, "fmt_deluser"))
        elif cmd in ("/promote", "/makeadmin"):
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            try:
                target = int(arg)
            except ValueError:
                send_msg(chat_id, t(L, "fmt_promote"))
                return
            admins.add(target)
            users.add(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "user_promoted", target=target))
            try:
                send_msg(target, t(get_lang(target), "admin_promoted_msg"))
            except Exception:
                pass
        elif cmd in ("/demote", "/unadmin"):
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            try:
                target = int(arg)
            except ValueError:
                send_msg(chat_id, t(L, "fmt_demote"))
                return
            if target == owner_id:
                send_msg(chat_id, t(L, "owner_no_demote"))
                return
            if target == uid:
                send_msg(chat_id, t(L, "self_no_demote"))
                return
            admins.discard(target)
            save_db(admins, users)
            send_msg(chat_id, t(L, "demoted", target=target))
        elif cmd == "/transfer":
            if uid != owner_id:
                send_msg(chat_id, t(L, "owner_only"))
                return
            try:
                target = int(arg)
            except ValueError:
                send_msg(chat_id, t(L, "fmt_transfer"))
                return
            if target == uid:
                send_msg(chat_id, t(L, "already_owner"))
                return
            api_call("sendMessage", {"chat_id": chat_id,
                                     "text": t(L, "transfer_confirm", target=target),
                                     "parse_mode": "HTML",
                                     "reply_markup": confirm_transfer_kb(target, L)})
            return
        elif cmd == "/users":
            if not is_admin(uid):
                send_msg(chat_id, t(L, "only_admin"))
                return
            lst = "\n".join(f"• <code>{x}</code>" + (" 👑" if x in admins else "") for x in sorted(users)) or t(L, "users_empty")
            send_msg(chat_id, t(L, "users_title", n=len(users), lst=lst) + t(L, "users_add_hint"))
        else:
            send_msg(chat_id, t(L, "unknown_cmd"))
        return
    # plain message → look for links
    links = re.findall(r"(?:https?://)?t\.me/\S+", text)
    if not links:
        send_msg(chat_id, t(L, "send_link_hint"))
        return
    for lnk in links[:5]:
        await handle_link(chat_id, uid, lnk)


async def poll_loop():
    global offset
    loop = asyncio.get_running_loop()
    while True:
        try:
            updates = await loop.run_in_executor(None, get_updates)
            for u in updates:
                offset = max(offset, u["update_id"] + 1)
                try:
                    await handle_update(u)
                except Exception as e:
                    log.exception("update err: %s", e)
        except Exception as e:
            log.warning("poll err: %s — retry in 3s", e)
            await asyncio.sleep(3)


async def main():
    me = await asyncio.get_running_loop().run_in_executor(None, api_call, "getMe")
    log.info("bot: @%s", me.get("username"))
    await init_userbot()
    await poll_loop()


if __name__ == "__main__":
    if "--check" in sys.argv:
        print(f"config OK (data={DATA_DIR})")
        raise SystemExit(0)
    asyncio.run(main())

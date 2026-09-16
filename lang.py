# -*- coding: utf-8 -*-
"""Trilingual strings: fa / en / ckb (Sorani Kurdish). Fallback language: fa."""

LANGS = ("fa", "en", "ckb")
DEFAULT = "fa"
LANG_NAMES = {"fa": "🇮🇷 فارسی", "en": "🇬🇧 English", "ckb": "☀️ کوردی"}

T = {
# ── language picker ──
"lang_pick": {
 "fa": "🌐 زبانت رو انتخاب کن / Choose your language / زمانەکەت هەڵبژێرە:",
 "en": "🌐 Choose your language / زبانت رو انتخاب کن / زمانەکەت هەڵبژێرە:",
 "ckb": "🌐 زمانەکەت هەڵبژێرە / زبانت رو انتخاب کن / Choose your language:",
},
"lang_set_ok": {
 "fa": "✅ زبان روی فارسی تنظیم شد.",
 "en": "✅ Language set to English.",
 "ckb": "✅ زمان کرایە کوردی.",
},
# ── buttons ──
"btn_login": {"fa": "🔑 ورود", "en": "🔑 Login", "ckb": "🔑 چوونەژوور"},
"btn_logout": {"fa": "🚪 خروج", "en": "🚪 Logout", "ckb": "🚪 دەرچوون"},
"btn_myid": {"fa": "🆔 آیدی من", "en": "🆔 My ID", "ckb": "🆔 ئایدی من"},
"btn_help": {"fa": "📖 راهنما", "en": "📖 Help", "ckb": "📖 یارمەتی"},
"btn_admin": {"fa": "👑 مدیریت", "en": "👑 Admin", "ckb": "👑 بەڕێوەبردن"},
"btn_menu": {"fa": "📋 منو", "en": "📋 Menu", "ckb": "📋 مێنیو"},
"btn_support": {"fa": "🆘 پشتیبانی", "en": "🆘 Support", "ckb": "🆘 پشتیوانی"},
"btn_lang": {"fa": "🌐 زبان", "en": "🌐 Language", "ckb": "🌐 زمان"},
"menu_title": {"fa": "📋 منو:", "en": "📋 Menu:", "ckb": "📋 مێنیو:"},
# ── help / start ──
"help_text": {
 "fa": ("📥 <b>راهنمای بات دانلودر</b>\n\n"
  "🔗 فقط <b>لینک پیام</b> رو بفرست:\n"
  "<code>https://t.me/channel/123</code>\n"
  "<code>https://t.me/c/123456/789</code>\n\n"
  "📷 عکس، 🎬 ویدیو، 📁 فایل و 📝 متن پشتیبانی میشه.\n"
  "⚠️ گروه/کانال خصوصی: یکی از اکانت‌های وصل باید عضوش باشه.\n"
  "🔑 با /login اکانت خودت رو وصل کن تا از گروه‌های خودت هم دانلود کنی.\n\n"
  "📌 دستورات:\n"
  "/login — اتصال اکانت خودت (QR یا کد)\n"
  "/logout — قطع اتصال اکانتت\n"
  "/myid — دیدن آیدی عددی خودت\n"
  "/lang — تغییر زبان\n"
  "/menu — نمایش منوی دکمه‌ای\n"
  "/support — 🆘 پشتیبانی (تیکت و چت زنده)\n"
  "/cancel — لغو ورود\n"
  "/help — همین راهنما\n\n"
  "👑 مدیرها از دکمه «👑 مدیریت» یا /admin استفاده کنن."),
 "en": ("📥 <b>Downloader Bot Guide</b>\n\n"
  "🔗 Just send a <b>message link</b>:\n"
  "<code>https://t.me/channel/123</code>\n"
  "<code>https://t.me/c/123456/789</code>\n\n"
  "📷 Photos, 🎬 videos, 📁 files and 📝 text are supported.\n"
  "⚠️ Private group/channel: one of the connected accounts must be a member.\n"
  "🔑 Use /login to connect your own account and download from your groups.\n\n"
  "📌 Commands:\n"
  "/login — connect your account (QR or code)\n"
  "/logout — disconnect your account\n"
  "/myid — show your numeric ID\n"
  "/lang — change language\n"
  "/menu — show button menu\n"
  "/support — 🆘 support (tickets & live chat)\n"
  "/cancel — cancel login\n"
  "/help — this guide\n\n"
  "👑 Admins: use the «👑 Admin» button or /admin."),
 "ckb": ("📥 <b>ڕێنمایی بۆتی داگرتن</b>\n\n"
  "🔗 تەنها <b>لینکی نامە</b> بنێرە:\n"
  "<code>https://t.me/channel/123</code>\n"
  "<code>https://t.me/c/123456/789</code>\n\n"
  "📷 وێنە، 🎬 ڤیدیۆ، 📁 فایل و 📝 دەق پشتیوانی دەکرێت.\n"
  "⚠️ گرووپ/کەناڵی تایبەت: یەکێک لە ئەکانتە پەیوەستەکان دەبێت ئەندام بێت.\n"
  "🔑 بە /login ئەکانتەکەت پەیوەست بکە بۆ داگرتن لە گرووپەکانی خۆت.\n\n"
  "📌 فەرمانەکان:\n"
  "/login — پەیوەستکردنی ئەکانت (QR یان کۆد)\n"
  "/logout — دابڕانی ئەکانت\n"
  "/myid — بینینی ئایدی ژمارەیی\n"
  "/lang — گۆڕینی زمان\n"
  "/menu — پیشاندانی مێنیو\n"
  "/support — 🆘 پشتیوانی (تیکت و چاتی زیندوو)\n"
  "/cancel — هەڵپەساردنی چوونەژوور\n"
  "/help — ئەم ڕێنماییە\n\n"
  "👑 بەڕێوەبەران: دوگمەی «👑 بەڕێوەبردن» یان /admin بەکاربهێنن."),
},
"hello": {
 "fa": "سلام! {role}\n\n{help}",
 "en": "Hello! {role}\n\n{help}",
 "ckb": "سڵاو! {role}\n\n{help}",
},
"role_admin": {"fa": "👑 مدیر", "en": "👑 Admin", "ckb": "👑 بەڕێوەبەر"},
"role_user": {"fa": "✅ کاربر", "en": "✅ User", "ckb": "✅ بەکارهێنەر"},
# ── admin panel ──
"admin_panel": {
 "fa": "👑 <b>پنل مدیریت</b>\nیکی رو انتخاب کن:",
 "en": "👑 <b>Admin panel</b>\nChoose one:",
 "ckb": "👑 <b>پانێڵی بەڕێوەبردن</b>\nیەکێک هەڵبژێرە:",
},
"adm_add": {"fa": "➕ افزودن کاربر", "en": "➕ Add user", "ckb": "➕ زیادکردنی بەکارهێنەر"},
"adm_del": {"fa": "➖ حذف کاربر", "en": "➖ Remove user", "ckb": "➖ سڕینەوەی بەکارهێنەر"},
"adm_list": {"fa": "👥 لیست کاربرها", "en": "👥 User list", "ckb": "👥 لیستی بەکارهێنەران"},
"adm_promote": {"fa": "⬆️ ارتقا به مدیر", "en": "⬆️ Promote to admin", "ckb": "⬆️ بەرزکردنەوە بۆ بەڕێوەبەر"},
"adm_demote": {"fa": "⬇️ عزل مدیر", "en": "⬇️ Demote admin", "ckb": "⬇️ دابەزاندنی بەڕێوەبەر"},
"adm_accounts": {"fa": "🔑 اکانت‌های وصل", "en": "🔑 Connected accounts", "ckb": "🔑 ئەکانتە پەیوەستەکان"},
"adm_transfer": {"fa": "👑 انتقال مالکیت", "en": "👑 Transfer ownership", "ckb": "👑 گواستنەوەی خاوەندارێتی"},
"transfer_yes": {"fa": "✅ تأیید انتقال", "en": "✅ Confirm transfer", "ckb": "✅ پشتڕاستکردنەوە"},
"transfer_no": {"fa": "❌ لغو", "en": "❌ Cancel", "ckb": "❌ هەڵپەساردن"},
# ── accounts ──
"accounts_title": {"fa": "🔑 اکانت‌های وصل:\n", "en": "🔑 Connected accounts:\n", "ckb": "🔑 ئەکانتە پەیوەستەکان:\n"},
"accounts_main": {"fa": "• اصلی: {nm}", "en": "• Main: {nm}", "ckb": "• سەرەکی: {nm}"},
"accounts_main_ok": {"fa": "• اصلی: وصل", "en": "• Main: connected", "ckb": "• سەرەکی: پەیوەستە"},
"accounts_user_ok": {"fa": "وصل", "en": "connected", "ckb": "پەیوەستە"},
"accounts_user_q": {"fa": "؟", "en": "?", "ckb": "؟"},
"accounts_none": {"fa": "هیچ اکانتی وصل نیست.", "en": "No account connected.", "ckb": "هیچ ئەکانتێک پەیوەست نییە."},
# ── access ──
"no_access": {
 "fa": "⛔ دسترسی نداری.\nآیدی تو: <code>{uid}</code>\nاین آیدی رو به مدیر بده.",
 "en": "⛔ No access.\nYour ID: <code>{uid}</code>\nSend this ID to the admin.",
 "ckb": "⛔ دەستت پێناگات.\nئایدی تۆ: <code>{uid}</code>\nئەم ئایدیە بە بەڕێوەبەر بدە.",
},
"only_admin": {
 "fa": "⛔ فقط مدیر.", "en": "⛔ Admins only.", "ckb": "⛔ تەنها بەڕێوەبەر.",
},
# ── login ──
"login_qr_chosen": {"fa": "📷 حالت QR انتخاب شد.", "en": "📷 QR mode selected.", "ckb": "📷 دۆخی QR هەڵبژێردرا."},
"login_phone_ask": {
 "fa": "📱 شماره‌ت رو با <b>+</b> بفرست:\nمثلاً <code>+98912...</code>",
 "en": "📱 Send your number with <b>+</b>:\ne.g. <code>+98912...</code>",
 "ckb": "📱 ژمارەکەت بە <b>+</b> بنێرە:\nبۆ نموونە <code>+98912...</code>",
},
"login_phone_ask_simple": {
 "fa": "📱 شماره‌ت رو با + بفرست:",
 "en": "📱 Send your number with +:",
 "ckb": "📱 ژمارەکەت بە + بنێرە:",
},
"qr_btn": {"fa": "📷 اسکن QR", "en": "📷 Scan QR", "ckb": "📷 سکانی QR"},
"code_btn": {"fa": "🔢 کد ورود", "en": "🔢 Login code", "ckb": "🔢 کۆدی چوونەژوور"},
"login_choose": {"fa": "🔑 روش ورود رو انتخاب کن:", "en": "🔑 Choose login method:", "ckb": "🔑 شێوازی چوونەژوور هەڵبژێرە:"},
"login_in_progress": {
 "fa": "⏳ یه ورود در جریانه؛ QR رو اسکن کن یا صبر کن تموم بشه.",
 "en": "⏳ A login is in progress; scan the QR or wait.",
 "ckb": "⏳ چوونەژوورێک لە ئارادایە؛ QR سکەن بکە یان چاوەڕوانبە.",
},
"login_qr_making": {"fa": "📷 دارم QR ورود می‌سازم...", "en": "📷 Generating login QR...", "ckb": "📷 QRی چوونەژوور دروست دەکەم..."},
"login_problem": {"fa": "❌ مشکلی پیش اومد. دوباره /login بزن.", "en": "❌ Something went wrong. Press /login again.", "ckb": "❌ کێشەیەک ڕوویدا. دووبارە /login بکە."},
"login_start_fail": {"fa": "❌ شروع ورود ناموفق: {e}", "en": "❌ Login failed to start: {e}", "ckb": "❌ دەستپێکی چوونەژوور سەرنەکەوت: {e}"},
"qr_caption": {
 "fa": "📷 با خودِ تلگرام اسکن کن (نه دوربین گوشی):\nتلگرام گوشی > تنظیمات ⚙️ > دستگاه‌ها > «اتصال دستگاه دسکتاپ»\n⏳ این کد حدود ۳۰ ثانیه اعتبار داره؛ اگه نشد خودش تازه میشه.",
 "en": "📷 Scan with Telegram itself (not your phone camera):\nPhone Telegram > Settings ⚙️ > Devices > «Link Desktop Device»\n⏳ This code is valid ~30 seconds; it refreshes automatically.",
 "ckb": "📷 بە خودی تێلێگرام سکەن بکە (نەک کامێرای مۆبایل):\nتێلێگرامی مۆبایل > ڕێکخستنەکان ⚙️ > ئامێرەکان > «پەیوەستکردنی ئامێری دێسکتۆپ»\n⏳ ئەم کۆدە نزیکەی ٣٠ چرکە بەسوودە؛ خۆی نوێ دەبێتەوە.",
},
"qr_send_fail": {"fa": "❌ ارسال QR ناموفق: {e}", "en": "❌ Failed to send QR: {e}", "ckb": "❌ ناردنی QR سەرنەکەوت: {e}"},
"qr_timeout": {"fa": "⌛ اسکن انجام نشد. دوباره /login بزن و سریع اسکن کن.", "en": "⌛ Not scanned. Press /login again and scan quickly.", "ckb": "⌛ سکەن نەکرا. دووبارە /login بکە و بەخێو سکەن بکە."},
"login_ok_groups": {
 "fa": "✅ اکانتت وصل شد ({nm})! حالا لینک پیام گروه‌هایی که عضوشی رو بفرست.",
 "en": "✅ Your account is connected ({nm})! Now send message links from your groups.",
 "ckb": "✅ ئەکانتەکەت پەیوەست بوو ({nm})! ئێستا لینکی نامەکانی گرووپەکانت بنێرە.",
},
"login_ok": {"fa": "✅ اکانتت وصل شد! حالا لینک پیام رو بفرست.", "en": "✅ Connected! Now send a message link.", "ckb": "✅ پەیوەست بوو! ئێستا لینکی نامە بنێرە."},
"login_connected": {
 "fa": "✅ اکانتت وصله ({nm}). اگه می‌خوای عوضش کنی اول /logout بزن.",
 "en": "✅ Your account is connected ({nm}). To change it, /logout first.",
 "ckb": "✅ ئەکانتەکەت پەیوەستە ({nm}). بۆ گۆڕینی، سەرەتا /logout بکە.",
},
"login_connected_simple": {"fa": "✅ اکانتت وصله.", "en": "✅ Your account is connected.", "ckb": "✅ ئەکانتەکەت پەیوەستە."},
"phone_invalid": {
 "fa": "❌ شماره نامعتبره. مثل این بفرست: <code>+98912...</code>",
 "en": "❌ Invalid number. Send like: <code>+98912...</code>",
 "ckb": "❌ ژمارە هەڵەیە. وەک ئەمە بنێرە: <code>+98912...</code>",
},
"login_sending_code": {"fa": "⏳ دارم کد می‌فرستم...", "en": "⏳ Sending code...", "ckb": "⏳ کۆد دەنێرم..."},
"login_flood": {
 "fa": "⏳ تلگرام محدودت کرده. کمی صبر کن و دوباره /login بزن.\n({e})",
 "en": "⏳ Telegram limited you. Wait a bit and press /login again.\n({e})",
 "ckb": "⏳ تێلێگرام سنوورداری کردوویت. کەمێک چاوەڕوانبە و دووبارە /login بکە.\n({e})",
},
"login_phone_fail": {"fa": "❌ شماره قبول نشد: {e}", "en": "❌ Number rejected: {e}", "ckb": "❌ ژمارە قبووڵ نەکرا: {e}"},
"code_sent": {
 "fa": "✅ کد ارسال شد!\n⚠️ کد رو با <b>حروف</b> بفرست (نه عدد!)، مثلاً:\n<code>پنج هشت نه نه نه</code>\n⏳ سریع بفرست (۲ دقیقه).",
 "en": "✅ Code sent!\n⚠️ Send the code in <b>words</b> (not digits!), e.g.:\n<code>five eight nine nine nine</code>\n⏳ Hurry (2 minutes).",
 "ckb": "✅ کۆد نێردرا!\n⚠️ کۆدەکە بە <b>وشە</b> بنێرە (نەک ژمارە!)، بۆ نموونە:\n<code>پێنج هەشت نۆ نۆ نۆ</code>\n⏳ بەخێو بنێرە (٢ خولەک).",
},
"code_unknown": {
 "fa": "❌ کد رو نفهمیدم. با حروف بفرست، مثلاً:\n<code>پنج هشت نه نه نه</code>",
 "en": "❌ Didn't get the code. Send in words, e.g.:\n<code>five eight nine nine nine</code>",
 "ckb": "❌ کۆدەکەم تێنەگەی. بە وشە بنێرە، بۆ نموونە:\n<code>پێنج هەشت نۆ نۆ نۆ</code>",
},
"pwd_need": {"fa": "🔐 روی اکانتت رمز دوم فعاله. رمز دوم رو بفرست:", "en": "🔐 Your account has 2FA. Send the second password:", "ckb": "🔐 لە ئەکانتەکەت وشەی نهێنی دووەم چالاکە. بینێرە:"},
"code_expired_new": {
 "fa": "⌛ کد قبلی منقضی شد؛ کد جدید فرستادم. با حروف و سریع بفرست:",
 "en": "⌛ Old code expired; sent a new one. Send in words, quickly:",
 "ckb": "⌛ کۆدی پێشوو بەسەرچوو؛ کۆدێکی نوێم نارد. بە وشە و بەخێو بنێرە:",
},
"code_resend_fail": {"fa": "❌ ارسال مجدد ناموفق: {e}", "en": "❌ Resend failed: {e}", "ckb": "❌ دووبارە ناردن سەرنەکەوت: {e}"},
"code_expired": {"fa": "⌛ کد منقضی شد. دوباره /login بزن.", "en": "⌛ Code expired. Press /login again.", "ckb": "⌛ کۆد بەسەرچوو. دووبارە /login بکە."},
"code_invalid": {"fa": "❌ کد اشتباهه. با حروف و با دقت بفرست:", "en": "❌ Wrong code. Send carefully in words:", "ckb": "❌ کۆد هەڵەیە. بە وردی بە وشە بنێرە:"},
"login_fail": {"fa": "❌ ورود ناموفق: {e}", "en": "❌ Login failed: {e}", "ckb": "❌ چوونەژوور سەرنەکەوت: {e}"},
"pwd_wrong": {"fa": "❌ رمز دوم اشتباهه. دوباره بفرست:", "en": "❌ Wrong 2FA password. Send again:", "ckb": "❌ وشەی نهێنی دووەم هەڵەیە. دووبارە بنێرە:"},
"login_cancelled": {"fa": "🚫 ورود لغو شد.", "en": "🚫 Login cancelled.", "ckb": "🚫 چوونەژوور هەڵپەسێردرا."},
"logged_out": {"fa": "👋 اتصال اکانتت قطع شد. (/login برای وصل مجدد)", "en": "👋 Your account is disconnected. (/login to reconnect)", "ckb": "👋 ئەکانتەکەت دابڕا. (/login بۆ دووبارە پەیوەستبوون)"},
"login_timeout": {"fa": "⌛ وقت تموم شد. دوباره /login بزن.", "en": "⌛ Timed out. Press /login again.", "ckb": "⌛ کات تەواو بوو. دووبارە /login بکە."},
# ── support ──
"sup_title": {"fa": "🆘 <b>پشتیبانی</b>\nیکی رو انتخاب کن:", "en": "🆘 <b>Support</b>\nChoose one:", "ckb": "🆘 <b>پشتیوانی</b>\nیەکێک هەڵبژێرە:"},
"sup_ticket": {"fa": "📝 ثبت تیکت", "en": "📝 New ticket", "ckb": "📝 تۆماری تیکت"},
"sup_chat": {"fa": "💬 چت زنده با مدیر", "en": "💬 Live chat with admin", "ckb": "💬 چاتی زیندوو لەگەڵ بەڕێوەبەر"},
"ticket_reply": {"fa": "✉️ پاسخ", "en": "✉️ Reply", "ckb": "✉️ وەڵام"},
"ticket_close": {"fa": "✅ بستن", "en": "✅ Close", "ckb": "✅ داخستن"},
"sup_ticket_ask": {"fa": "📝 مشکلت رو تو یه پیام بفرست تا تیکت بشه:", "en": "📝 Send your issue in one message to make a ticket:", "ckb": "📝 کێشەکەت لە نامەیەکدا بنێرە بۆ تیکت:"},
"sup_ticket_ask_simple": {"fa": "📝 مشکلت رو بفرست:", "en": "📝 Send your issue:", "ckb": "📝 کێشەکەت بنێرە:"},
"sup_chat_ok": {
 "fa": "💬 به چت زنده وصل شدی! پیامت رو بفرست.\n(لینک بفرستی دانلود میشه)\n/end برای پایان چت.",
 "en": "💬 Connected to live chat! Send your message.\n(Links get downloaded)\n/end to end the chat.",
 "ckb": "💬 بە چاتی زیندوو پەیوەست بوویت! نامەکەت بنێرە.\n(لینک دابەزێنرێت)\n/end بۆ کۆتایی چات.",
},
"sup_chat_ok_simple": {
 "fa": "💬 به چت وصل شدی! پیامت رو بفرست. /end برای پایان.",
 "en": "💬 Connected! Send your message. /end to end.",
 "ckb": "💬 پەیوەست بوویت! نامەکەت بنێرە. /end بۆ کۆتایی.",
},
"sup_chat_admin": {"fa": "💬 کاربر <code>{uid}</code> چت زنده خواست.", "en": "💬 User <code>{uid}</code> requested live chat.", "ckb": "💬 بەکارهێنەر <code>{uid}</code> چاتی زیندووی داواکرد."},
"ticket_reply_ask": {"fa": "✉️ پاسخ تیکت #{nid} رو بفرست:", "en": "✉️ Send your reply to ticket #{nid}:", "ckb": "✉️ وەڵامی تیکت #{nid} بنێرە:"},
"ticket_closed": {"fa": "🎫 تیکت #{nid} بسته شد ✅", "en": "🎫 Ticket #{nid} closed ✅", "ckb": "🎫 تیکت #{nid} داخرا ✅"},
"ticket_closed_user": {"fa": "🔒 تیکت #{nid} بسته شد.", "en": "🔒 Ticket #{nid} is closed.", "ckb": "🔒 تیکت #{nid} داخرا."},
"ticket_not_found": {"fa": "❌ تیکت پیدا نشد.", "en": "❌ Ticket not found.", "ckb": "❌ تیکت نەدۆزرایەوە."},
"ticket_answered": {"fa": "✅ پاسخت به تیکت #{ar} رسید.", "en": "✅ Your reply to ticket #{ar} was delivered.", "ckb": "✅ وەڵامەکەت بۆ تیکت #{ar} گەیەندرا."},
"ticket_user_reply": {"fa": "✉️ <b>پاسخ تیکت #{ar}:</b>\n\n{text}", "en": "✉️ <b>Reply to ticket #{ar}:</b>\n\n{text}", "ckb": "✉️ <b>وەڵامی تیکت #{ar}:</b>\n\n{text}"},
"ticket_line": {
 "fa": "• #{nid} [{st}] از <code>{uid}</code>: {txt}",
 "en": "• #{nid} [{st}] from <code>{uid}</code>: {txt}",
 "ckb": "• #{nid} [{st}] لە <code>{uid}</code>: {txt}",
},
"ticket_created": {
 "fa": "✅ تیکتت ثبت شد! شماره: <b>#{nid}</b>\nمدیر جواب بده خبرت می‌کنم.",
 "en": "✅ Ticket created! Number: <b>#{nid}</b>\nI'll tell you when an admin replies.",
 "ckb": "✅ تیکتەکەت تۆمارکرا! ژمارە: <b>#{nid}</b>\nکاتێک بەڕێوەبەر وەڵامداتەوە ئاگادارت دەکەمەوە.",
},
"ticket_new": {"fa": "🎫 <b>تیکت #{nid}</b> از <code>{uid}</code>:\n\n{text}", "en": "🎫 <b>Ticket #{nid}</b> from <code>{uid}</code>:\n\n{text}", "ckb": "🎫 <b>تیکت #{nid}</b> لە <code>{uid}</code>:\n\n{text}"},
"tickets_open": {"fa": "🎫 تیکت‌های باز:\n{lines}", "en": "🎫 Open tickets:\n{lines}", "ckb": "🎫 تیکتە کراوەکان:\n{lines}"},
"tickets_none": {"fa": "📭 تیکت بازی نیست.", "en": "📭 No open tickets.", "ckb": "📭 هیچ تیکتێکی کراوە نییە."},
"support_reply": {"fa": "💬 <b>پاسخ پشتیبانی:</b>\n{text}", "en": "💬 <b>Support reply:</b>\n{text}", "ckb": "💬 <b>وەڵامی پشتیوانی:</b>\n{text}"},
"msg_delivered": {"fa": "✅ پیامت به کاربر رسید.", "en": "✅ Delivered to the user.", "ckb": "✅ بە بەکارهێنەر گەیەندرا."},
"send_fail": {"fa": "❌ ارسال ناموفق: {e}", "en": "❌ Send failed: {e}", "ckb": "❌ ناردن سەرنەکەوت: {e}"},
"chat_reply_hint": {
 "fa": "❌ به پیام «💬 چت زنده» ریپلای کن (Reply) تا جوابت به کاربر برسه.",
 "en": "❌ Reply to the «💬 live chat» message so your answer reaches the user.",
 "ckb": "❌ وەڵامی نامەی «💬 چاتی زیندوو» بدەرەوە بۆ گەیاندن بە بەکارهێنەر.",
},
"chat_expired": {"fa": "⌛ چت منقضی شد. برای شروع دوباره /support بزن.", "en": "⌛ Chat expired. Press /support to start again.", "ckb": "⌛ چات بەسەرچوو. بۆ دووبارە /support بکە."},
"chat_live": {"fa": "💬 <b>چت زنده</b> از <code>{uid}</code>:\n\n{text}", "en": "💬 <b>Live chat</b> from <code>{uid}</code>:\n\n{text}", "ckb": "💬 <b>چاتی زیندوو</b> لە <code>{uid}</code>:\n\n{text}"},
"chat_closed": {"fa": "👋 چت بسته شد.", "en": "👋 Chat closed.", "ckb": "👋 چات داخرا."},
"chat_closed_user": {"fa": "👋 کاربر <code>{uid}</code> چت رو بست.", "en": "👋 User <code>{uid}</code> closed the chat.", "ckb": "👋 بەکارهێنەر <code>{uid}</code> چاتی داخست."},
"chat_closed_admin": {"fa": "👋 مدیر چت رو بست.", "en": "👋 Admin closed the chat.", "ckb": "👋 بەڕێوەبەر چاتی داخست."},
"no_active_chat": {"fa": "چت فعالی نداری. /support برای شروع.", "en": "No active chat. /support to start.", "ckb": "هیچ چاتێکی چالاکت نییە. /support بۆ دەستپێک."},
# ── admin user management ──
"users_title": {"fa": "👥 کاربرها ({n}):\n{lst}", "en": "👥 Users ({n}):\n{lst}", "ckb": "👥 بەکارهێنەران ({n}):\n{lst}"},
"users_empty": {"fa": "خالی", "en": "empty", "ckb": "بەتاڵ"},
"users_add_hint": {"fa": "\n\n➕ افزودن: <code>/adduser آیدی</code>", "en": "\n\n➕ Add: <code>/adduser id</code>", "ckb": "\n\n➕ زیادکردن: <code>/adduser ئایدی</code>"},
"adm_add_ask": {
 "fa": "➕ آیدی عددی کاربر جدید رو بفرست:\n(طرف با /myid می‌تونه آیدیش رو ببینه)",
 "en": "➕ Send the new user's numeric ID:\n(They can see it with /myid)",
 "ckb": "➕ ئایدی ژمارەیی بەکارهێنەری نوێ بنێرە:\n(بە /myid دەیبینێت)",
},
"adm_del_ask": {"fa": "➖ آیدی عددی کاربری که حذف بشه رو بفرست:", "en": "➖ Send the numeric ID to remove:", "ckb": "➖ ئایدی ژمارەیی بۆ سڕینەوە بنێرە:"},
"adm_promote_ask": {"fa": "⬆️ آیدی عددی کسی که مدیر بشه رو بفرست:", "en": "⬆️ Send the numeric ID to promote:", "ckb": "⬆️ ئایدی ژمارەیی بۆ بەرزکردنەوە بنێرە:"},
"adm_demote_ask": {"fa": "⬇️ آیدی عددی مدیری که عزل بشه رو بفرست:", "en": "⬇️ Send the admin ID to demote:", "ckb": "⬇️ ئایدی بەڕێوەبەر بۆ دابەزاندن بنێرە:"},
"only_owner": {"fa": "⛔ فقط مالک فعلی", "en": "⛔ Current owner only.", "ckb": "⛔ تەنها خاوەنی ئێستا."},
"transfer_ask": {
 "fa": "👑 <b>انتقال مالکیت کامل</b>\nآیدی عددی مالک جدید رو بفرست.\n⚠️ بعد از تأیید، مالکیت کامل منتقل میشه!",
 "en": "👑 <b>Full ownership transfer</b>\nSend the new owner's numeric ID.\n⚠️ After confirm, full ownership moves!",
 "ckb": "👑 <b>گواستنەوەی تەواوی خاوەندارێتی</b>\nئایدی ژمارەیی خاوەنی نوێ بنێرە.\n⚠️ دوای پشتڕاستکردنەوە، خاوەندارێتی تەواو دەگوازرێتەوە!",
},
"transfer_done": {
 "fa": "👑 مالکیت کامل به <code>{target}</code> منتقل شد!\nتو ادمین موندی.",
 "en": "👑 Ownership moved to <code>{target}</code>!\nYou stayed admin.",
 "ckb": "👑 خاوەندارێتی بۆ <code>{target}</code> گوازرایەوە!\nتۆ بە بەڕێوەبەر مایتەوە.",
},
"transfer_new": {"fa": "👑 مالک کامل بات دانلودر شدی! /admin", "en": "👑 You are now the owner of the downloader bot! /admin", "ckb": "👑 ئێستا تۆ خاوەنی بۆتی داگرتنی! /admin"},
"transfer_cancelled": {"fa": "🚫 انتقال مالکیت لغو شد.", "en": "🚫 Transfer cancelled.", "ckb": "🚫 گواستنەوە هەڵپەسێردرا."},
"transfer_confirm": {
 "fa": "👑 انتقال مالکیت کامل به <code>{target}</code>؟\n⚠️ مطمئنی؟",
 "en": "👑 Transfer full ownership to <code>{target}</code>?\n⚠️ Sure?",
 "ckb": "👑 خاوەندارێتی تەواو بۆ <code>{target}</code> بگوازرێتەوە؟\n⚠️ دڵنیایت؟",
},
"owner_transfer_only": {
 "fa": "⛔ فقط مالک فعلی می‌تونه مالکیت رو منتقل کنه.",
 "en": "⛔ Only the current owner can transfer ownership.",
 "ckb": "⛔ تەنها خاوەنی ئێستا دەتوانێت بیگوازێتەوە.",
},
"already_owner": {"fa": "❌ خودت مالکی!", "en": "❌ You are already the owner!", "ckb": "❌ خۆت خاوەنیت!"},
"owner_only": {"fa": "⛔ فقط مالک فعلی.", "en": "⛔ Current owner only.", "ckb": "⛔ تەنها خاوەنی ئێستا."},
"id_not_found": {
 "fa": "❌ آیدی عددی پیدا نکردم. از پنل دوباره تلاش کن.",
 "en": "❌ No numeric ID found. Try from the panel again.",
 "ckb": "❌ ئایدی ژمارەیی نەدۆزرایەوە. لە پانێڵەوە دووبارە هەوڵبدە.",
},
"user_added": {"fa": "✅ کاربر <code>{target}</code> اضافه شد.", "en": "✅ User <code>{target}</code> added.", "ckb": "✅ بەکارهێنەر <code>{target}</code> زیادکرا."},
"user_added_msg": {"fa": "✅ به بات دانلودر اضافه شدی! /start", "en": "✅ You were added to the downloader bot! /start", "ckb": "✅ بۆ بۆتی داگرتن زیادکرایت! /start"},
"user_promoted": {"fa": "👑 کاربر <code>{target}</code> مدیر شد.", "en": "👑 User <code>{target}</code> is now admin.", "ckb": "👑 بەکارهێنەر <code>{target}</code> بوو بە بەڕێوەبەر."},
"admin_promoted_msg": {"fa": "👑 تو بات دانلودر مدیر شدی! /admin", "en": "👑 You are now a downloader bot admin! /admin", "ckb": "👑 ئێستا تۆ بەڕێوەبەری بۆتی داگرتنی! /admin"},
"owner_no_demote": {"fa": "❌ نمیشه مالک رو عزل کرد.", "en": "❌ Can't demote the owner.", "ckb": "❌ ناکرێت خاوەن داببەزێنرێت."},
"self_no_demote": {"fa": "❌ خودت رو نمی‌تونی عزل کنی.", "en": "❌ You can't demote yourself.", "ckb": "❌ ناتوانیت خۆت داببەزێنیت."},
"not_admin": {"fa": "❌ این آیدی مدیر نیست.", "en": "❌ This ID is not an admin.", "ckb": "❌ ئەم ئایدیە بەڕێوەبەر نییە."},
"demoted": {"fa": "⬇️ مدیر <code>{target}</code> عزل شد (کاربر معمولی موند).", "en": "⬇️ Admin <code>{target}</code> demoted (stays a user).", "ckb": "⬇️ بەڕێوەبەر <code>{target}</code> دابەزێنرا (وەک بەکارهێنەر دەمێنێتەوە)."},
"owner_no_delete": {"fa": "❌ نمیشه مالک رو حذف کرد.", "en": "❌ Can't remove the owner.", "ckb": "❌ ناکرێت خاوەن بسڕدرێتەوە."},
"user_deleted": {"fa": "🗑 کاربر <code>{target}</code> حذف شد.", "en": "🗑 User <code>{target}</code> removed.", "ckb": "🗑 بەکارهێنەر <code>{target}</code> سڕایەوە."},
"fmt_adduser": {"fa": "❌ فرمت: <code>/adduser 123456</code>", "en": "❌ Format: <code>/adduser 123456</code>", "ckb": "❌ فۆرمات: <code>/adduser 123456</code>"},
"fmt_deluser": {"fa": "❌ فرمت: <code>/deluser 123456</code>", "en": "❌ Format: <code>/deluser 123456</code>", "ckb": "❌ فۆرمات: <code>/deluser 123456</code>"},
"fmt_promote": {"fa": "❌ فرمت: <code>/promote آیدی</code>", "en": "❌ Format: <code>/promote id</code>", "ckb": "❌ فۆرمات: <code>/promote ئایدی</code>"},
"fmt_demote": {"fa": "❌ فرمت: <code>/demote آیدی</code>", "en": "❌ Format: <code>/demote id</code>", "ckb": "❌ فۆرمات: <code>/demote ئایدی</code>"},
"fmt_transfer": {"fa": "❌ فرمت: <code>/transfer آیدی</code>", "en": "❌ Format: <code>/transfer id</code>", "ckb": "❌ فۆرمات: <code>/transfer ئایدی</code>"},
# ── misc commands ──
"myid_is": {"fa": "🆔 آیدی تو: <code>{uid}</code>", "en": "🆔 Your ID: <code>{uid}</code>", "ckb": "🆔 ئایدی تۆ: <code>{uid}</code>"},
"unknown_cmd": {"fa": "❓ دستور نامشخص. /help", "en": "❓ Unknown command. /help", "ckb": "❓ فەرمانی نەناسراو. /help"},
"send_link_hint": {"fa": "🔗 لینک پیام رو بفرست. /help", "en": "🔗 Send a message link. /help", "ckb": "🔗 لینکی نامە بنێرە. /help"},
# ── download flow ──
"fetch_join_fail": {"fa": "دسترسی به کانال ممکن نیست: {e}", "en": "Cannot access channel: {e}", "ckb": "دەستگەیشتن بە کەناڵ نەکرا: {e}"},
"msg_not_found": {"fa": "پیام پیدا نشد (شاید پاک شده).", "en": "Message not found (maybe deleted).", "ckb": "نامە نەدۆزرایەوە (ڕەنگە سڕابێتەوە)."},
"msg_empty": {"fa": "این پیام هیچ فایل/عکس/متن نداره.", "en": "This message has no file/photo/text.", "ckb": "ئەم نامەیە هیچ فایل/وێنە/دەقێکی نییە."},
"dl_fail": {"fa": "دانلود ناموفق بود.", "en": "Download failed.", "ckb": "داگرتن سەرنەکەوت."},
"no_account_first": {
 "fa": "⚠️ هیچ اکانتی وصل نیست. اول /login بزن و اکانتت رو وصل کن.",
 "en": "⚠️ No account connected. First /login and connect your account.",
 "ckb": "⚠️ هیچ ئەکانتێک پەیوەست نییە. سەرەتا /login بکە و ئەکانتەکەت پەیوەست بکە.",
},
"joining": {"fa": "⏳ در حال عضو کردن اکانت...", "en": "⏳ Joining the account...", "ckb": "⏳ ئەکانت ئەندام دەکرێت..."},
"joined_ok": {"fa": "✅ اکانت عضو شد! حالا لینک پیام رو بفرست.", "en": "✅ Joined! Now send the message link.", "ckb": "✅ ئەکانت ئەندام بوو! ئێستا لینکی نامە بنێرە."},
"already_member": {"fa": "✅ قبلاً عضو بوده! حالا لینک پیام رو بفرست.", "en": "✅ Already a member! Now send the message link.", "ckb": "✅ پێشتر ئەندام بووە! ئێستا لینکی نامە بنێرە."},
"invite_bad": {"fa": "❌ لینک دعوت نامعتبر یا منقضی شده.", "en": "❌ Invite link invalid or expired.", "ckb": "❌ لینکی بانگهێشتن هەڵە یان بەسەرچووە."},
"join_fail": {"fa": "❌ عضویت ناموفق: {e}", "en": "❌ Join failed: {e}", "ckb": "❌ ئەندامبوون سەرنەکەوت: {e}"},
"link_bad": {
 "fa": "❌ لینک نامعتبره. مثال:\n<code>https://t.me/channel/123</code>",
 "en": "❌ Bad link. Example:\n<code>https://t.me/channel/123</code>",
 "ckb": "❌ لینک هەڵەیە. نموونە:\n<code>https://t.me/channel/123</code>",
},
"no_account_qr": {
 "fa": "⚠️ هیچ اکانتی وصل نیست. /login بزن و با QR اکانتت رو وصل کن، بعد لینک بده.",
 "en": "⚠️ No account connected. /login with QR first, then send the link.",
 "ckb": "⚠️ هیچ ئەکانتێک پەیوەست نییە. بە QR /login بکە، پاشان لینک بنێرە.",
},
"downloading": {"fa": "⏳ در حال دانلود...", "en": "⏳ Downloading...", "ckb": "⏳ دادەبەزێنرێت..."},
"text_msg": {"fa": "📝 متن پیام:\n\n{txt}", "en": "📝 Message text:\n\n{txt}", "ckb": "📝 دەقی نامە:\n\n{txt}"},
"heavy_sent": {"fa": "✅ فایل سنگین بود، مستقیم ارسال شد 👆", "en": "✅ File was big, sent directly 👆", "ckb": "✅ فایل گەورە بوو، ڕاستەوخۆ نێردرا 👆"},
"not_member": {
 "fa": "❌ هیچ‌کدوم از اکانت‌های وصل عضو این چت خصوصی نیستن.\nلینک دعوت رو بفرست تا عضو بشن، یا با /login اکانت عضوش رو وصل کن.",
 "en": "❌ None of the connected accounts are in this private chat.\nSend the invite link to join them, or /login with a member account.",
 "ckb": "❌ هیچ یەک لە ئەکانتە پەیوەستەکان لەم چاتە تایبەتەدا نین.\nلینکی بانگهێشتن بنێرە بۆ ئەندامبوون، یان بە /login ئەکانتێکی ئەندام پەیوەست بکە.",
},
"err": {"fa": "❌ خطا: {e}", "en": "❌ Error: {e}", "ckb": "❌ هەڵە: {e}"},
}


def get(lang, key):
    """Return template for lang with fa fallback."""
    d = T.get(key, {})
    return d.get(lang) or d.get(DEFAULT) or key

# ربات دانلودر تلگرام 📥 (کانال‌ها و گروه‌های خصوصی)

> 🇬🇧 [English guide](README.md)

رباتی که از کانال‌ها و گروه‌های **خصوصی/بسته‌شده (restricted)** دانلود می‌کنه.
ربات‌ها به محتوای ضدفوروارد دسترسی ندارن، پس این پروژه دو بخش داره: ربات معمولی
(دسترسی کاربرها، منوها، ارسال مجدد فایل) + یوزربات Telethon (اکانت خودت) که
دانلود واقعی رو انجام میده.

**سه‌زبانه:** 🇮🇷 فارسی · 🇬🇧 English · ☀️ کوردی — موقع `/start` انتخاب می‌کنی و
بعداً با دکمه 🌐 یا دستور `/lang` عوضش می‌کنی.

## امکانات

- 📷 عکس، 🎬 ویدیو، 📁 فایل و 📝 متن فقط با لینک پیام:
  `https://t.me/channel/123` و `https://t.me/c/123456/789`
- 🔗 لینک دعوت (`t.me/+hash`): اول اکانت رو عضو می‌کنه، بعد لینک پیام رو می‌فرستی
- 🔑 ورود جدا برای هر کاربر: اسکن **QR** یا **کد ورود** (کد رو با *حروف* می‌فرستی،
  نه عدد) + پشتیبانی از رمز دوم
- 👑 پنل مدیریت: افزودن/حذف کاربر، ارتقا/عزل مدیر، اکانت‌های وصل، انتقال کامل مالکیت
- 🆘 پشتیبانی: تیکت + چت زنده با مدیر
- 📦 فایل‌های بالای ~۴۸ مگ مستقیم با اکانت ارسال میشن (محدودیت API دور زده میشه)
- 🔄 سرویس systemd + واچ‌داگ cron + حلقه اجرای خودکار

## نصب با یک دستور (سرور تازه اوبونتو/دبیان، با دسترسی root)

```bash
curl -sSL https://raw.githubusercontent.com/nalascityboy-afk/telegram-downloader-bot/main/install.sh | sudo bash
```

نصاب فقط ۴ چیز می‌پرسه (هیچ رازی داخل گیت ذخیره نمیشه):

| سوال | از کجا بگیرم |
|---|---|
| توکن ربات | [@BotFather](https://t.me/BotFather) ← دستور `/newbot` |
| API ID و API HASH | [my.telegram.org](https://my.telegram.org) ← بخش API development tools |
| آیدی عددی مالک | به هر رباتی `/myid` بده یا از [@userinfobot](https://t.me/userinfobot) بپرس |

بعدش کانفیگ رو تست می‌کنه (`bot.py --check`)، سرویس systemd و واچ‌داگ ۵دقیقه‌ای
رو فعال می‌کنه. ربات رو باز کن، **/start** بزن، زبان رو انتخاب کن، بعد با
**/login** اکانت تلگرامت رو وصل کن (برای QR: تنظیمات ← دستگاه‌ها ← اتصال دستگاه
دسکتاپ).

## نصب دستی

```bash
git clone https://github.com/nalascityboy-afk/telegram-downloader-bot.git
cd telegram-downloader-bot
python3 -m venv venv && ./venv/bin/python -m pip install -r requirements.txt
cp .env.example .env   # بعد .env رو پر کن
./venv/bin/python bot.py --check   # باید "config OK" چاپ کنه
nohup bash run_bot.sh >/dev/null 2>&1 &
# واچ‌داگ (اختیاری): */5 * * * * bash /path/to/check_bot.sh
```

تنظیمات داخل `.env` هست (نمونه: `.env.example`). متغیرهای لازم:

- `RESTRICTED_BOT_TOKEN` ،`TG_API_ID` ،`TG_API_HASH` ،`BOT_OWNER_ID`
- اختیاری: `DATA_DIR` (پیش‌فرض `./data`) و `DL_DIR` (پیش‌فرض `<DATA_DIR>/downloads`)

## طرز استفاده

۱. `/start` ← انتخاب زبان ← راهنما و منوی دکمه‌ای میاد.
۲. `/login` ← با QR یا کد ← اکانتت وصل میشه.
   (چت خصوصی فقط وقتی کار می‌کنه که **تو** یا اکانت اپراتور عضوش باشه.
   اگه اکانت باید جوین بشه، اول لینک دعوت رو بفرست.)
۳. لینک پیام رو بفرست ← ربات دانلود می‌کنه و فایل رو همین‌جا تحویلت میده.
۴. `/logout` اتصال اکانت رو قطع می‌کنه. `/support` تیکت و چت زنده‌ست.

دستورهای مدیر: پنل `/admin` ،`/adduser` ،`/deluser` ،`/promote` ،`/demote` ،
`/transfer` ،`/users` ،`/tickets` ،`/accounts` ،`/lang`.

## به‌روزرسانی

```bash
cd /opt/downloader-bot && git pull && ./venv/bin/pip install -r requirements.txt \
  && sudo systemctl restart downloader-bot
```

## رفع اشکال

- خطای `Missing required env var` ← فایل `.env` ناقصه؛ نصاب رو دوباره اجرا کن یا `.env` رو دستی پر کن.
- `userbot NOT authorized` داخل لاگ ← داخل ربات `/login` بزن و دوباره وصل شو.
- `NOTMEMBER` / «عضو این چت خصوصی نیست» ← با `/login` اکانتِ عضو رو وصل کن یا
  لینک دعوت بفرست تا اکانت اپراتور جوین بشه.
- `PhoneCodeExpiredError` ← کد ~۲ دقیقه اعتبار داره؛ ربات یک‌بار خودش
  دوباره می‌فرسته، بعدش `/login` رو از اول بزن.
- فایل‌های سنگین «مستقیم» از اکانت میان — این مسیر بالای ۴۸ مگه، باگ نیست.
- خطای `database is locked` ← دو پروسس روی یک `.session` هستن؛ فقط یک نمونه
  اجرا کن (systemd خودش همین کار رو می‌کنه).

## نکته‌های امنیتی

- هیچ‌وقت `.env` و فایل‌های `*.session` رو کامیت نکن — داخل `.gitignore` هستن.
- کد ورود رو داخل تلگرام حتماً با **حروف** بفرست (عدد رو خود تلگرام برای همون
  اکانت رد می‌کنه).
- اگه توکن/سشن لو رفت: از [@BotFather](https://t.me/BotFather) با `/revoke`
  باطلش کن و سشن‌ها رو از تنظیمات تلگرام ← دستگاه‌ها ببند.

## ساختار فایل‌ها

- `bot.py` — منطق ربات + یوزربات (کانفیگ env، handlers)
- `lang.py` — رشته‌های فارسی/انگلیسی/کردی (کلیدِ جاافتاده به فارسی برمی‌گرده)
- `run_bot.sh` — اجرای خودکار · `check_bot.sh` — واچ‌داگ cron
- `install.sh` — نصب تک‌دستوری سرور · `requirements.txt`

لایسنس MIT — فایل [LICENSE](LICENSE).

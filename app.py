"""
app.py
نسخه‌ی «تک‌رباتی» برای فروش/تحویل به مشتری.
مشتری با متغیر محیطی PLATFORM مشخص می‌کند کدام ربات اجرا شود
(بدون این‌که هیچ خط کدی را ببیند یا تغییر دهد).
"""

import os
from dotenv import load_dotenv

from core import instagram, youtube, tiktok, pinterest
from core.bot_factory import build_bot
from keep_alive import keep_alive

load_dotenv()

PLATFORM_MODULES = {
    "instagram": instagram,
    "youtube": youtube,
    "tiktok": tiktok,
    "pinterest": pinterest,
}


def main():
    platform = os.getenv("PLATFORM", "").strip().lower()
    token = os.getenv("BOT_TOKEN", "").strip()

    if platform not in PLATFORM_MODULES:
        raise SystemExit(
            f"❌ مقدار PLATFORM باید یکی از این‌ها باشد: {', '.join(PLATFORM_MODULES)} "
            f"(مقدار فعلی: '{platform}')"
        )
    if not token:
        raise SystemExit("❌ متغیر BOT_TOKEN تنظیم نشده است.")

    keep_alive()
    module = PLATFORM_MODULES[platform]
    free_use_limit = int(os.getenv("FREE_USE_LIMIT", "0") or "0")
    contact_info = os.getenv("SELLER_CONTACT", "")
    bot = build_bot(token, module, free_use_limit=free_use_limit, contact_info=contact_info)
    print(f"✅ ربات {module.PLATFORM_NAME} روشن شد.")
    bot.infinite_polling(timeout=60, long_polling_timeout=60)


if __name__ == "__main__":
    main()

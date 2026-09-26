"""bot_insta.py — ربات دانلود اینستاگرام. این فایل به‌همراه core/ قابل فروش/تحویل جداگانه است."""

import os
from dotenv import load_dotenv

from core import instagram
from core.bot_factory import build_bot

load_dotenv()


def start_insta_bot():
    token = os.getenv("INSTA_BOT_TOKEN")
    if not token:
        print("⚠️  INSTA_BOT_TOKEN تنظیم نشده — ربات اینستاگرام روشن نشد.")
        return

    free_use_limit = int(os.getenv("FREE_USE_LIMIT", "0") or "0")
    contact_info = os.getenv("SELLER_CONTACT", "")

    bot = build_bot(token, instagram, free_use_limit=free_use_limit, contact_info=contact_info)
    print("✅ ربات اینستاگرام روشن شد.")
    bot.infinite_polling(timeout=60, long_polling_timeout=60)


if __name__ == "__main__":
    start_insta_bot()

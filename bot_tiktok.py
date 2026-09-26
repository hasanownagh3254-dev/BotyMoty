"""bot_tiktok.py — ربات دانلود تیک‌تاک. این فایل به‌همراه core/ قابل فروش/تحویل جداگانه است."""

import os
from dotenv import load_dotenv

from core import tiktok
from core.bot_factory import build_bot

load_dotenv()


def start_tiktok_bot():
    token = os.getenv("TIKTOK_BOT_TOKEN")
    if not token:
        print("⚠️  TIKTOK_BOT_TOKEN تنظیم نشده — ربات تیک‌تاک روشن نشد.")
        return

    free_use_limit = int(os.getenv("FREE_USE_LIMIT", "0") or "0")
    contact_info = os.getenv("SELLER_CONTACT", "")

    bot = build_bot(token, tiktok, free_use_limit=free_use_limit, contact_info=contact_info)
    print("✅ ربات تیک‌تاک روشن شد.")
    bot.infinite_polling(timeout=60, long_polling_timeout=60)


if __name__ == "__main__":
    start_tiktok_bot()

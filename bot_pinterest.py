"""bot_pinterest.py — ربات دانلود پینترست. این فایل به‌همراه common.py، bot_factory.py و ماژول همون پلتفرم قابل فروش/تحویل جداگانه است."""

import os
from dotenv import load_dotenv

import pinterest
from bot_factory import build_bot

load_dotenv()


def start_pinterest_bot():
    token = os.getenv("PINTEREST_BOT_TOKEN")
    if not token:
        print("⚠️  PINTEREST_BOT_TOKEN تنظیم نشده — ربات پینترست روشن نشد.")
        return

    free_use_limit = int(os.getenv("FREE_USE_LIMIT", "0") or "0")
    contact_info = os.getenv("SELLER_CONTACT", "")

    bot = build_bot(token, pinterest, free_use_limit=free_use_limit, contact_info=contact_info)
    print("✅ ربات پینترست روشن شد.")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


if __name__ == "__main__":
    start_pinterest_bot()

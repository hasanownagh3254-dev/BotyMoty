"""
main.py
همه‌ی ربات‌ها را هم‌زمان (هرکدام در یک Thread) روشن می‌کند.
اگر یکی از ربات‌ها به‌دلیل خطا از کار بیفتد، به‌تنهایی و خودکار دوباره استارت می‌شود
— بدون این‌که بقیه‌ی ربات‌ها خاموش شوند.
"""

import time
import threading

from keep_alive import keep_alive
from bot_insta import start_insta_bot
from bot_youtube import start_yt_bot
from bot_tiktok import start_tiktok_bot
from bot_pinterest import start_pinterest_bot

BOTS = [
    ("اینستاگرام", start_insta_bot),
    ("یوتیوب", start_yt_bot),
    ("تیک‌تاک", start_tiktok_bot),
    ("پینترست", start_pinterest_bot),
]


def run_with_restart(name, target):
    while True:
        try:
            target()
        except Exception as e:
            print(f"⚠️  ربات {name} با خطا متوقف شد: {e}")
        print(f"🔁 تلاش دوباره برای روشن‌کردن ربات {name} تا ۱۰ ثانیه‌ی دیگر...")
        time.sleep(10)


if __name__ == "__main__":
    keep_alive()

    threads = []
    for name, target in BOTS:
        t = threading.Thread(target=run_with_restart, args=(name, target), daemon=True)
        t.start()
        threads.append(t)
        print(f"🚀 ربات {name} استارت شد.")

    print("همه‌ی ربات‌ها با موفقیت روشن شدند ✅")

    for t in threads:
        t.join()

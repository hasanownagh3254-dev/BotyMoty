"""
main.py
فایل اصلی اجرای هم‌زمان ربات‌ها روی سرور Render
"""

import os
import threading
import time
from core.bot_factory import build_bot
import core.instagram as instagram
import core.youtube as youtube
import core.tiktok as tiktok
import core.pinterest as pinterest
from keep_alive import keep_alive

# روشن نگه داشتن وب‌سرویس برای UptimeRobot
keep_alive()

BOT_CONFIGS = [
    {
        "name": "اینستاگرام",
        "token": os.getenv("INSTAGRAM_BOT_TOKEN"),
        "module": instagram,
    },
    {
        "name": "یوتیوب",
        "token": os.getenv("YOUTUBE_BOT_TOKEN"),
        "module": youtube,
    },
    {
        "name": "تیک‌تاک",
        "token": os.getenv("TIKTOK_BOT_TOKEN"),
        "module": tiktok,
    },
    {
        "name": "پینترست",
        "token": os.getenv("PINTEREST_BOT_TOKEN"),
        "module": pinterest,
    },
]

# تنظیم محدودیت ۲ بار استفاده برای نسخه‌ی تست
FREE_LIMIT = 2
CONTACT_INFO = "@your_username"  # آیدی تلگرام خودت را اینجا بنویس


def run_bot(config):
    token = config["token"]
    name = config["name"]

    if not token:
        print(f"⚠️ توکن مربوط به ربات {name} یافت نشد (اسکیپ شد).")
        return

    while True:
        try:
            bot = build_bot(
                token=token,
                platform_module=config["module"],
                free_use_limit=FREE_LIMIT,
                contact_info=CONTACT_INFO,
            )
            print(f"🚀 ربات {name} استارت شد...")
            # اصلاح متد اجرا: infinity_polling با حرف y
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"⚠️ ربات {name} با خطا متوقف شد: {e}")
            print(f"🔄 تلاش دوباره برای روشن‌کردن ربات {name} تا ۱۰ ثانیه‌ی دیگر...")
            time.sleep(10)


if __name__ == "__main__":
    threads = []
    for config in BOT_CONFIGS:
        t = threading.Thread(target=run_bot, args=(config,))
        t.daemon = True
        t.start()
        threads.append(t)

    print("✅ همه‌ی ربات‌ها با موفقیت روشن شدند.")

    for t in threads:
        t.join()
        

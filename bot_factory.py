"""
bot_factory.py
یک ربات تلگرام کامل (با /start و مدیریت خطا) از روی توکن و ماژول پلتفرم می‌سازد.
همه‌ی ربات‌ها (اینستاگرام، یوتیوب، تیک‌تاک، پینترست) از همین یک تابع ساخته می‌شوند.

اگر free_use_limit بزرگ‌تر از صفر باشد، ربات به «حالت دمو» می‌رود: هر کاربر فقط
همان تعداد بار می‌تواند دانلود موفق بگیرد و بعدش پیام دعوت‌به‌خرید می‌بیند.
free_use_limit=0 (پیش‌فرض) یعنی بدون محدودیت — برای ربات‌های فروخته‌شده.
"""

import telebot

from common import (
    cleanup_file,
    DownloadError,
    try_acquire_download_slot,
    wait_for_download_slot,
    release_download_slot,
)
from usage_limiter import has_free_uses_left, increment_usage, get_usage


def build_bot(token: str, platform_module, free_use_limit: int = 0, contact_info: str = ""):
    """
    token: توکن ربات از BotFather
    platform_module: یکی از instagram / youtube / tiktok / pinterest
    free_use_limit: تعداد دفعات مجاز استفاده‌ی رایگان برای هر کاربر (۰ = نامحدود)
    contact_info: متنی که در پیام «دوره‌ی آزمایشی تمام شد» نشان داده می‌شود (مثلاً آیدی تلگرام فروشنده)
    خروجی: یک شیء TeleBot آماده‌ی اجرا
    """
    bot = telebot.TeleBot(token, parse_mode=None)
    platform_name = platform_module.PLATFORM_NAME

    def limit_reached_text() -> str:
        base = "🚫 این ربات جهت تست بوده و برای مالکیت آن باید ربات را خریداری کنید."
        if contact_info:
            base += f"\nبرای خرید پیام بده: {contact_info}"
        return base

    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message):
        text = f"سلام 👋\nلینک ویدیوی {platform_name} رو برام بفرست تا برات دانلودش کنم."
        if free_use_limit > 0:
            remaining = max(0, free_use_limit - get_usage(message.from_user.id))
            text += f"\n\n🎁 این نسخه‌ی آزمایشیه؛ {remaining} بار دیگه می‌تونی رایگان امتحانش کنی."
        bot.reply_to(message, text)

    @bot.message_handler(func=lambda m: True)
    def handle_message(message):
        url = (message.text or "").strip()

        if not platform_module.is_valid_url(url):
            bot.reply_to(message, f"❌ این یک لینک معتبر {platform_name} نیست.")
            return

        user_id = message.from_user.id
        if not has_free_uses_left(user_id, free_use_limit):
            bot.reply_to(message, limit_reached_text())
            return

        status = bot.reply_to(message, "⏳ در حال دانلود، چند لحظه صبر کن...")
        filepath = None

        got_slot_now = try_acquire_download_slot()
        if not got_slot_now:
            bot.edit_message_text(
                "🕐 سرور در حال حاضر شلوغه. تو صف منتظر بمون، به‌محض آزادشدن ظرفیت شروع می‌شه...",
                message.chat.id,
                status.message_id,
            )
            wait_for_download_slot()
            bot.edit_message_text("⏳ نوبتت رسید، در حال دانلود...", message.chat.id, status.message_id)

        try:
            filepath = platform_module.download(url)
            with open(filepath, "rb") as video_file:
                bot.send_video(message.chat.id, video_file, timeout=180)
            bot.delete_message(message.chat.id, status.message_id)
            if free_use_limit > 0:
                increment_usage(user_id)
        except DownloadError as e:
            bot.edit_message_text(f"❌ {e}", message.chat.id, status.message_id)
        except Exception as e:
            bot.edit_message_text(
                f"❌ خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کن.\n({e})",
                message.chat.id,
                status.message_id,
            )
        finally:
            release_download_slot()
            cleanup_file(filepath)

    return bot

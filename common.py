"""
common.py
موتور مشترک دانلود که همه‌ی ماژول‌های پلتفرم (اینستاگرام، یوتیوب، تیک‌تاک) از آن استفاده می‌کنند.
اگر روزی yt-dlp رفتار خودش را تغییر داد، فقط همین یک فایل نیاز به اصلاح دارد.
"""

import os
import time
import logging
import tempfile
import threading

import yt_dlp

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# تلگرام اجازه‌ی آپلود بالای ۵۰ مگابایت رو نمی‌ده؛ ۴۵ مگ می‌ذاریم که یک حاشیه‌ی امن باشه
MAX_TELEGRAM_FILE_SIZE = 45 * 1024 * 1024

# روی پلن رایگان Render فقط ۵۱۲ مگابایت رم هست. هر دانلود هم‌زمان حافظه مصرف می‌کند،
# پس تعداد دانلودهای هم‌زمان (بین همه‌ی ربات‌ها در این پروسه) را محدود می‌کنیم.
# درخواست‌های اضافه به‌جای کرش‌کردن سرور، در صف منتظر می‌مانند.
MAX_CONCURRENT_DOWNLOADS = int(os.environ.get("MAX_CONCURRENT_DOWNLOADS", "2"))
_download_slots = threading.Semaphore(MAX_CONCURRENT_DOWNLOADS)


def try_acquire_download_slot() -> bool:
    """بدون صبر کردن چک می‌کند جای خالی هست یا نه. True یعنی جا رزرو شد."""
    return _download_slots.acquire(blocking=False)


def wait_for_download_slot():
    """منتظر می‌ماند تا یک جای خالی آزاد شود (یعنی کاربر در صف قرار می‌گیرد)."""
    _download_slots.acquire(blocking=True)


def release_download_slot():
    _download_slots.release()


class DownloadError(Exception):
    """خطای قابل‌نمایش به کاربر (پیام فارسی و قابل‌فهم)."""
    pass


def download_video(url: str, max_retries: int = 2) -> str:
    """
    ویدیو را از لینک داده‌شده دانلود می‌کند.
    خروجی: مسیر فایل دانلودشده روی دیسک.
    در صورت شکست، DownloadError پرتاب می‌شود.
    """
    download_dir = tempfile.mkdtemp(prefix="dl_")

    ydl_opts = {
        "outtmpl": os.path.join(download_dir, "%(id)s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": MAX_TELEGRAM_FILE_SIZE,
    }

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

                if not os.path.exists(filepath):
                    raise DownloadError("فایل دانلودشده پیدا نشد. لینک را بررسی کنید.")

                size = os.path.getsize(filepath)
                if size > MAX_TELEGRAM_FILE_SIZE:
                    os.remove(filepath)
                    raise DownloadError(
                        "حجم این ویدیو بیشتر از ۴۵ مگابایت است و تلگرام اجازه‌ی "
                        "ارسال آن از طریق ربات را نمی‌دهد."
                    )
                return filepath

        except DownloadError:
            raise
        except Exception as e:
            last_error = e
            logger.warning(f"تلاش {attempt} برای {url} ناموفق بود: {e}")
            time.sleep(1.5)

    raise DownloadError(
        "دانلود این لینک ناموفق بود. ممکن است لینک خصوصی، حذف‌شده یا نامعتبر باشد."
    )


def cleanup_file(filepath: str):
    """فایل موقت و پوشه‌ی خالی‌شده را پاک می‌کند تا فضای دیسک پر نشود."""
    try:
        if filepath and os.path.exists(filepath):
            parent = os.path.dirname(filepath)
            os.remove(filepath)
            if parent and os.path.isdir(parent) and not os.listdir(parent):
                os.rmdir(parent)
    except Exception as e:
        logger.warning(f"خطا در پاک‌سازی فایل {filepath}: {e}")

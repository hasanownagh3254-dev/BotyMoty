"""
core/usage_limiter.py
شمارنده‌ی ساده‌ی تعداد استفاده‌ی هر کاربر، برای ربات‌های "دمو/تستی" که برای خریدارهای
احتمالی می‌گذاری تا امتحان کنند. روی یک فایل JSON کنار کد ذخیره می‌شود.

⚠️ محدودیت مهم: روی پلن رایگان Render دیسک همیشه پایدار نیست — اگر سرویس Redeploy
یا کاملاً ری‌استارت شود، این فایل ممکن است پاک شود و شمارش از صفر شروع شود. برای یک
دموی ساده که فقط می‌خواهی جلوی سوءاستفاده‌ی معمولی را بگیری کافی‌ست، ولی ۱۰۰٪ غیرقابل‌دور‌زدن نیست.
"""

import json
import os
import threading

_LOCK = threading.Lock()


def _usage_file_path() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "usage_data.json")


def _load() -> dict:
    path = _usage_file_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: dict):
    with open(_usage_file_path(), "w", encoding="utf-8") as f:
        json.dump(data, f)


def get_usage(user_id: int) -> int:
    with _LOCK:
        return _load().get(str(user_id), 0)


def increment_usage(user_id: int) -> int:
    with _LOCK:
        data = _load()
        key = str(user_id)
        data[key] = data.get(key, 0) + 1
        _save(data)
        return data[key]


def has_free_uses_left(user_id: int, limit: int) -> bool:
    """limit=0 یعنی بدون محدودیت (برای ربات‌های فروخته‌شده/نامحدود)."""
    if limit <= 0:
        return True
    return get_usage(user_id) < limit

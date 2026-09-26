"""tiktok.py — منطق مخصوص تیک‌تاک."""

from common import download_video, DownloadError

PLATFORM_NAME = "تیک‌تاک"


def is_valid_url(url: str) -> bool:
    return "tiktok.com" in url


def download(url: str) -> str:
    if not is_valid_url(url):
        raise DownloadError("این یک لینک معتبر تیک‌تاک نیست.")
    return download_video(url)

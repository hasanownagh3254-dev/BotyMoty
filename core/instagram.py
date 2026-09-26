"""core/instagram.py — منطق مخصوص اینستاگرام."""

from core.common import download_video, DownloadError

PLATFORM_NAME = "اینستاگرام"


def is_valid_url(url: str) -> bool:
    return "instagram.com" in url


def download(url: str) -> str:
    if not is_valid_url(url):
        raise DownloadError("این یک لینک معتبر اینستاگرام نیست.")
    return download_video(url)

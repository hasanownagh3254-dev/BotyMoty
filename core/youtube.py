"""core/youtube.py — منطق مخصوص یوتیوب."""

from core.common import download_video, DownloadError

PLATFORM_NAME = "یوتیوب"


def is_valid_url(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url


def download(url: str) -> str:
    if not is_valid_url(url):
        raise DownloadError("این یک لینک معتبر یوتیوب نیست.")
    return download_video(url)

"""pinterest.py — منطق مخصوص پینترست."""

from common import download_video, DownloadError

PLATFORM_NAME = "پینترست"


def is_valid_url(url: str) -> bool:
    return "pinterest.com" in url or "pin.it" in url


def download(url: str) -> str:
    if not is_valid_url(url):
        raise DownloadError("این یک لینک معتبر پینترست نیست.")
    return download_video(url)

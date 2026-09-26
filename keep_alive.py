"""
keep_alive.py
یک وب‌سرور کوچک Flask که Render آن را به‌عنوان "سرویس زنده" می‌شناسد
و UptimeRobot با پینگ‌کردن آن، از خواب‌رفتن سرویس رایگان جلوگیری می‌کند.
"""

import os
import threading
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "ربات‌ها روشن و در حال اجرا هستند ✅"


def _run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = threading.Thread(target=_run, daemon=True)
    t.start()

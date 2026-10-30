import os
import sys
import requests

token = os.getenv("BOT_TOKEN", "").strip()
webhook_url = os.getenv("WEBHOOK_URL", "").strip()
secret = os.getenv("WEBHOOK_SECRET", "").strip()

if not token or not webhook_url or not secret:
    sys.exit("Set BOT_TOKEN, WEBHOOK_URL and WEBHOOK_SECRET environment variables first.")

response = requests.post(
    f"https://api.telegram.org/bot{token}/setWebhook",
    json={
        "url": webhook_url.rstrip("/") + "/webhook",
        "secret_token": secret,
        "drop_pending_updates": False,
    },
    timeout=20,
)
print(response.text)
response.raise_for_status()

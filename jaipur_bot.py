import os, time, requests
from datetime import datetime
import pytz

API_KEY = os.getenv("DELTA_KEY")
API_SECRET = os.getenv("DELTA_SECRET")

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except:
        pass

print("Jaipur Hunter Bot Started - Safe Mode")
ist = pytz.timezone('Asia/Kolkata')
while True:
    now = datetime.now(ist).strftime("%H:%M:%S")
    print(f"Bot running... {now} - Waiting for setup")
    time.sleep(60)

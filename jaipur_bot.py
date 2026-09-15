import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Jaipur Hunter Bot LIVE - Monitoring Jaipur!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Start web server for Render
Thread(target=run_web, daemon=True).start()

# --- YOUR BOT CODE STARTS BELOW ---

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

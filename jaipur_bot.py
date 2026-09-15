import os
import time
import threading
import hmac
import hashlib
import json
import requests
import pytz
from datetime import datetime
from flask import Flask, request
import telebot

# === CONFIG FROM RENDER ENVIRONMENT ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "8396092843:AAGUURdCJLFxkD_xPKWnJ9X26dDHzbC6q0A")
API_KEY = os.getenv("DELTA_API_KEY", "YOUR_DELTA_API_KEY_HERE")
API_SECRET = os.getenv("DELTA_API_SECRET", "YOUR_DELTA_API_SECRET_HERE")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "") # Your personal chat id for alerts

PRODUCT_ID = int(os.getenv("PRODUCT_ID", "27")) # 27=BTCUSD
QTY = 1
BASE_URL = "https://api.india.delta.exchange"
ist = pytz.timezone("Asia/Kolkata")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# === DELTA FUNCTIONS ===
def delta_request(method, path, payload=""):
    if "YOUR_DELTA" in API_KEY:
        print("Delta API Keys not set yet", flush=True)
        return {}
    timestamp = str(int(time.time()))
    signature_data = method + timestamp + path + payload
    signature = hmac.new(API_SECRET.encode(), signature_data.encode(), hashlib.sha256).hexdigest()
    headers = {'api-key': API_KEY, 'timestamp': timestamp, 'signature': signature, 'Content-Type': 'application/json'}
    url = BASE_URL + path
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, timeout=10)
        else:
            r = requests.post(url, headers=headers, data=payload, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Delta Error: {e}", flush=True)
        return {}

def place_order():
    payload = {"product_id": PRODUCT_ID, "size": QTY, "side": "sell", "order_type": "market_order"}
    res = delta_request("POST", "/v2/orders", json.dumps(payload))
    print(f"{datetime.now(ist)} - SELL ENTRY -> {res}", flush=True)
    if TELEGRAM_CHAT_ID:
        try: bot.send_message(TELEGRAM_CHAT_ID, f"✅ Jaipur Hunter ENTRY Done at 9:20 AM\n{res}")
        except: pass
    return res

def close_all():
    payload = {"close_all_portfolio": False, "close_all_isolated": True, "product_ids": [PRODUCT_ID]}
    res = delta_request("POST", "/v2/positions/close_all", json.dumps(payload))
    print(f"{datetime.now(ist)} - EXIT -> {res}", flush=True)
    if TELEGRAM_CHAT_ID:
        try: bot.send_message(TELEGRAM_CHAT_ID, f"🔚 Jaipur Hunter EXIT Done at 5:30 PM\n{res}")
        except: pass
    return res

# === FLASK WEBHOOK ===
@app.route('/')
def home():
    return "Jaipur Hunter Bot Live - Trading + Telegram OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"Webhook Error: {e}", flush=True)
    return 'ok', 200

# === TELEGRAM COMMANDS ===
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👋 Jaipur Hunter Active!\n\nStrategy: SELL 76000 CE+PE at 9:20 AM\nEXIT at 5:30 PM IST\n\nCommands:\n/status - Check bot\nUse /setchat to set alert ID")

@bot.message_handler(commands=['status'])
def status(m):
    now = datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S IST")
    bot.reply_to(m, f"✅ Bot Live\nTime: {now}\nProduct: {PRODUCT_ID}\nQty: {QTY}")

@bot.message_handler(commands=['setchat'])
def setchat(m):
    bot.reply_to(m, f"Your CHAT_ID is: {m.chat.id}\nAdd this in Render Environment as CHAT_ID")

# === TRADING LOOP IN BACKGROUND THREAD ===
def trading_loop():
    print("Trading Loop Started", flush=True)
    entered_today = False
    while True:
        try:
            now = datetime.now(ist)
            hm = now.strftime("%H:%M")
            if hm == "09:20" and not entered_today:
                place_order()
                entered_today = True
                time.sleep(65)
            if hm == "17:30" and entered_today:
                close_all()
                entered_today = False
                time.sleep(65)
            if hm == "00:01":
                entered_today = False
            time.sleep(10)
        except Exception as e:
            print(f"Loop Error: {e}", flush=True)
            time.sleep(10)

threading.Thread(target=trading_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

import os, time, threading, requests, logging
from flask import Flask, request
from datetime import datetime
import pytz

# --- ENV ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "8396092843:AAGUURdCJLFxkD_xPKWnJ9X26dDHzbC6q0A")
DELTA_API_KEY = os.getenv("DELTA_API_KEY", "")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET", "")
CHAT_ID = os.getenv("CHAT_ID", "")  # will be set after /setchat

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

def send_message(chat_id, text):
    if not chat_id: return
    try:
        requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
        print(f"Sent to {chat_id}: {text[:50]}")
    except Exception as e:
        print(f"Send error: {e}")

def send_to_owner(text):
    # send to saved CHAT_ID if available
    if CHAT_ID:
        send_message(CHAT_ID, text)

# --- YOUR STRATEGY ---
def place_strategy_orders():
    # --- PUT YOUR DELTA LOGIC HERE ---
    # This runs at 9:20 AM IST
    try:
        msg = "🔥 Jaipur Hunter ENTRY: SELL 76000 CE + PE executed (simulated) at 9:20 AM"
        print(msg)
        # TODO: Add your Delta API sell code here using DELTA_API_KEY/SECRET
        send_to_owner(msg)
    except Exception as e:
        send_to_owner(f"Entry error: {e}")

def exit_strategy_orders():
    try:
        msg = "✅ Jaipur Hunter EXIT: All positions squared off at 5:30 PM"
        print(msg)
        # TODO: Add your Delta API exit code here
        send_to_owner(msg)
    except Exception as e:
        send_to_owner(f"Exit error: {e}")

def scheduler_loop():
    print("Scheduler started...")
    while True:
        try:
            now = datetime.now(IST)
            # 9:20 AM Entry
            if now.hour == 9 and now.minute == 20 and now.second < 10:
                place_strategy_orders()
                time.sleep(60)
            # 5:30 PM Exit = 17:30
            if now.hour == 17 and now.minute == 30 and now.second < 10:
                exit_strategy_orders()
                time.sleep(60)
        except Exception as e:
            print(f"Scheduler error: {e}")
        time.sleep(5)

# Start scheduler in background
threading.Thread(target=scheduler_loop, daemon=True).start()

# --- FLASK + TELEGRAM WEBHOOK ---
@app.route("/")
def home():
    return "Jaipur Hunter Bot is LIVE ✅ - Strategy + Telegram Active"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Update received: {data}")
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        t = text.lower().strip()
        if t.startswith("/start"):
            send_message(chat_id, "👋 Jaipur Hunter Active!\n\nStrategy: SELL 76000 CE+PE at 9:20 AM\nEXIT at 5:30 PM IST\n\nCommands:\n/setchat - get your CHAT_ID\n/status - check bot status")
        elif t.startswith("/setchat"):
            send_message(chat_id, f"Your CHAT_ID is: {chat_id}\n\nGo to Render -> Environment -> Add:\nCHAT_ID = {chat_id}\nThen Save.")
        elif t.startswith("/status"):
            send_message(chat_id, f"✅ Bot LIVE\nTime IST: {datetime.now(IST)}\nAPI Key set: {bool(DELTA_API_KEY)}\nOwner CHAT_ID set: {bool(CHAT_ID)}")
        else:
            send_message(chat_id, f"You said: {text}\nBot working ✅ Use /start")
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

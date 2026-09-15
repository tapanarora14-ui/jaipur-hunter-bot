import os
from flask import Flask, request
import telebot

BOT_TOKEN = "8396092843:AAGUURdCJLFxkD_xPKWnJ9X26dDHzbC6q0A"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🏹 Jaipur Hunter Bot LIVE!\n\nYour bot is WORKING ✅\n\nSend /hunt")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, f"You: {m.text}\nBot ONLINE ✅")

@app.route('/')
def home():
    return "Jaipur Hunter Bot Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

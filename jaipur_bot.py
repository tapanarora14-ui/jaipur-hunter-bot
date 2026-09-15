import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👨‍🍳 Welcome to Jaipur Hunter!\n\nSend any food name - biryani, pizza, chai etc.")

@bot.message_handler(func=lambda m: True)
def hunt(message):
    bot.reply_to(message, f"🔍 Hunting '{message.text}' in Jaipur...\n\n1. Tapri - C Scheme\n2. Jaipur Modern - MI Road\n3. Nibs - Malviya Nagar")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

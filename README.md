# telegram-bot
from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("8275267623:AAHiZ9ur7B8xQYSaCRRpYgBttXf2aK4JMEs")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Bot 24/7 ishlayapti ✅")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Webhook bot online 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

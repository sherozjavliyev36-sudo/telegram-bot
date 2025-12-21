import os
from flask import Flask, request
import telebot

# Render'dan o'zgaruvchilarni olish
TOKEN = os.environ.get('BOT_TOKEN')
URL = os.environ.get('RENDER_EXTERNAL_URL')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot 24/7 ishlayapti ✅")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + '/' + TOKEN)
    return "Webhook sozlandi!", 200

if __name__ == "__main__":
    # Render uchun portni to'g'ri sozlash
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

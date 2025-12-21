import os
from flask import Flask, request
import telebot

# Render sozlamalaridan xavfsiz olinadigan token
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Render avtomatik beradigan havola
URL = os.environ.get('RENDER_EXTERNAL_URL')

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Botingiz Webhook orqali 24/7 ishlamoqda! ✅")

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
    return "Webhook sozlandi! Botingiz tayyor.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

import os
import telebot
from flask import Flask, request
import yt_dlp

TOKEN = os.environ.get('BOT_TOKEN')
URL = os.environ.get('RENDER_EXTERNAL_URL')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def download_and_send(url, message):
    # Yuklash sozlamalari
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'max_filesize': 48000000, # 48MB limit
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="Tayyor! ✅ @sizning_botingiz")
        os.remove('video.mp4') # Serverni tozalash
    except Exception as e:
        bot.reply_to(message, "Xatolik: Video juda katta yoki havola noto'g'ri.")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Menga Youtube, Instagram yoki Pinterest havolasini yuboring. 📥")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    links = ['youtube.com', 'youtu.be', 'instagram.com', 'pinterest.com', 'pin.it']
    if any(domain in message.text for domain in links):
        bot.reply_to(message, "Xabar qabul qilindi. Yuklashni boshladim... ⏳")
        download_and_send(message.text, message)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + '/' + TOKEN)
    return "Downloader Bot Tayyor!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

import os
import telebot
from flask import Flask, request
import yt_dlp

TOKEN = os.environ.get('BOT_TOKEN')
URL = os.environ.get('RENDER_EXTERNAL_URL')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Yuklash funksiyasi
def download_and_send(url, message):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'max_filesize': 45000000, # 45MB dan oshiq fayllarni yuklamaydi (Render limiti)
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="Tayyor! ✅")
        os.remove('video.mp4')
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: Fayl juda katta bo'lishi mumkin.")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Menga Youtube, Instagram yoki Pinterest havolasini yuboring, men uni yuklab beraman! 📥")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    links = ['youtube.com', 'youtu.be', 'instagram.com', 'pinterest.com', 'pin.it']
    if any(link in message.text for link in links):
        bot.reply_to(message, "Havola qabul qilindi. Yuklashni boshladim... ⏳")
        download_and_send(message.text, message)
    else:
        bot.reply_to(message, "Iltimos, faqat video havolasini yuboring.")

# Render Webhook sozlamalari
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
    return "Bot Downloader holatida ishga tushdi!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

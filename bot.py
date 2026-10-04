import os
import telebot
import yt_dlp

BOT_TOKEN = "7963236750:AAFnW58gqgW1m6E78X-j6w2sBqC1P8o5m-k"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🔥 مرحباً بك في بوت AN Downloader\n\n"
        "⚡ أرسل لي أي رابط فيديو (TikTok, Instagram, YouTube, Facebook, Twitter, Shorts) وسأقوم بتحميله وإرساله لك فوراً بجودة عالية وبدون علامة مائية."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if not (url.startswith('http://') or url.startswith('https://')):
        bot.reply_to(message, "⚠️️ يرجى إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    status_msg = bot.reply_to(message, "⏳ جاري فحص الرابط وتحميل الفيديو... برجاء الانتظار.")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
        'quiet': True,
        'no_warnings': True
    }

    try:
        os.makedirs('downloads', exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            bot.edit_message_text("📤 جاري رفع الفيديو إليك الآن...", message.chat.id, status_msg.message_id)
            with open(filename, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption="✅ تم التحميل بواسطة @andownloader_bot")
            os.remove(filename)
            bot.delete_message(message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ حدث خطأ أثناء معالجة الملف.", message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text("❌ تعذر تحميل الفيديو. تأكد أن الرابط عام وحجم الفيديو أقل من 50 ميجابايت.", message.chat.id, status_msg.message_id)

print("Bot is running...")
bot.infinity_polling()

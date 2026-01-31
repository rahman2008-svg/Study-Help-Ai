import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# আপনার এপিআই কী এবং টোকেন
GEMINI_API_KEY = "AIzaSyDInMEDhlsfBhTnpE3VW7TdC9Y7mzLDnpY"
TELEGRAM_BOT_TOKEN = "8516062464:AAHBjjOfArYXf6-xsfjuCXGN9kUAA5Wi3gQ"

# Gemini AI কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash')

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# আপনার দেওয়া পরিচয়সহ /start কমান্ডের উত্তর
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "আসসালামু আলাইকুম! আমি Study Help AI।\n"
        "আমাকে তৈরি করেছেন Abdur Rahman।\n"
        "আমি আপনাকে কীভাবে সাহায্য করতে পারি?"
    )
    await update.message.reply_text(welcome_msg)

# এআই চ্যাট হ্যান্ডলার (ব্যবহারকারীর প্রশ্নের উত্তর দিবে)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Gemini 3 Flash মডেল থেকে রেসপন্স নেওয়া
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("দুঃখিত, এআই সার্ভারে সংযোগ করতে সমস্যা হচ্ছে। অনুগ্রহ করে কিছুক্ষণ পর চেষ্টা করুন।")

if __name__ == '__main__':
    # টেলিগ্রাম বট অ্যাপ্লিকেশন তৈরি
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # কমান্ড এবং মেসেজ হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Study Help AI বটটি চালু হয়েছে...")
    application.run_polling()
    

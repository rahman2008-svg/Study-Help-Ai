import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import os
from groq import Groq

# আপনার এপিআই কী এবং টোকেন
GROQ_API_KEY = "Gsk_RP4NZfgBSoEziEdHSqc0WGdyb3FY5LoZU9PSjTNIwRN4niHNQZhb"
TELEGRAM_BOT_TOKEN = "8516062464:AAHBjjOfArYXf6-xsfjuCXGN9kUAA5Wi3gQ"

# Groq ক্লায়েন্ট সেটআপ
client = Groq(api_key=GROQ_API_KEY)

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# আপনার দেওয়া পরিচয়সহ /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "আসসালামু আলাইকুম! আমি Study Help AI।\n"
        "আমাকে তৈরি করেছেন Abdur Rahman।\n"
        "আমি আপনাকে কীভাবে সাহায্য করতে পারি?"
    )
    await update.message.reply_text(welcome_msg)

# Groq AI দিয়ে মেসেজ হ্যান্ডল করা
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Groq মডেল কল করা (llama-3.3-70b বর্তমানে বেশ জনপ্রিয়)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_text}],
            model="llama-3.3-70b-versatile",
        )
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("দুঃখিত, বর্তমানে এআই সার্ভারে সমস্যা হচ্ছে।")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Study Help AI (Groq) চালু হয়েছে...")
    application.run_polling()
    

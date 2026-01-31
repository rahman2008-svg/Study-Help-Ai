import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from openai import OpenAI

# আপনার দেওয়া টোকেন এবং কী
XAI_API_KEY = "Xai-RgXFFAXO3mGmxsSSOc4GXZ31C9AEADiaCW70YGUnX3Dtv2qPeqGSiI8PGv9HIJLDFa9doqCWMp287J1z"
TELEGRAM_BOT_TOKEN = "8516062464:AAHBjjOfArYXf6-xsfjuCXGN9kUAA5Wi3gQ"

# Grok (xAI) ক্লায়েন্ট সেটআপ
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! আমি আপনার Grok AI বট। আমাকে যা খুশি জিজ্ঞাসা করুন।")

# মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Grok মডেল থেকে উত্তর আনা
        response = client.chat.completions.create(
            model="grok-beta", # অথবা "grok-2"
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, বর্তমানে একটি সমস্যা হচ্ছে। হয়তো API ক্রেডিটে সমস্যা।")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("বট চালু হচ্ছে...")
    application.run_polling()
  

"""
Simple test handler to verify bot is receiving messages
"""
import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, Application
from config.settings import settings
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or settings.TELEGRAM_BOT_TOKEN

async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple test handler"""
    print(f"✅ TEST HANDLER RECEIVED /start FROM {update.effective_user.id}", flush=True)
    await update.message.reply_text("✅ البوت يعمل! تم استقبال أمر /start")

async def main():
    """Test the bot"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add simple test handler
    app.add_handler(CommandHandler("start", test_start))
    
    print("🚀 Test bot started", flush=True)
    print(f"Token: {TELEGRAM_BOT_TOKEN[:20]}...", flush=True)
    
    # Run polling for testing
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

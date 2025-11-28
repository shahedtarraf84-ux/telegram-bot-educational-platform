"""
Script to get your Telegram ID
Run this to find your telegram_id
"""
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Your bot token
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's telegram ID"""
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    text = f"""
🆔 **معلوماتك:**

👤 الاسم: {first_name}
📱 Username: @{username if username else 'لا يوجد'}
🔢 Telegram ID: `{user_id}`

---

✅ **لجعل نفسك Admin:**

1. افتح ملف `.env`
2. أضف هذا السطر:
   ```
   TELEGRAM_ADMIN_ID={user_id}
   ```
3. احفظ الملف
4. أعد تشغيل البوت

🎉 ستصبح Admin!
    """
    
    await update.message.reply_text(text)
    print(f"\n{'='*50}")
    print(f"User: {first_name}")
    print(f"Username: @{username if username else 'N/A'}")
    print(f"Telegram ID: {user_id}")
    print(f"{'='*50}\n")
    print(f"Add this to .env file:")
    print(f"TELEGRAM_ADMIN_ID={user_id}")
    print(f"{'='*50}\n")


def build_application() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", get_my_id))
    app.add_handler(CommandHandler("id", get_my_id))
    return app

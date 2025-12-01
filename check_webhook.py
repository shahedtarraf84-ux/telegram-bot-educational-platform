#!/usr/bin/env python3
"""Check Telegram webhook status"""
import asyncio
import os
from telegram import Bot
from config.settings import settings

async def check_webhook():
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or settings.TELEGRAM_BOT_TOKEN
    bot = Bot(token=token)
    
    try:
        # Get webhook info
        webhook_info = await bot.get_webhook_info()
        print("=" * 60)
        print("🔍 WEBHOOK STATUS")
        print("=" * 60)
        print(f"URL: {webhook_info.url}")
        print(f"Has Custom Certificate: {webhook_info.has_custom_certificate}")
        print(f"Pending Update Count: {webhook_info.pending_update_count}")
        print(f"IP Address: {webhook_info.ip_address}")
        print(f"Last Error Date: {webhook_info.last_error_date}")
        print(f"Last Error Message: {webhook_info.last_error_message}")
        print(f"Last Synchronization Error Date: {webhook_info.last_synchronization_error_date}")
        print(f"Max Connections: {webhook_info.max_connections}")
        print(f"Allowed Updates: {webhook_info.allowed_updates}")
        print("=" * 60)
        
        # Check if webhook is set
        if webhook_info.url:
            print("✅ Webhook is SET")
            if webhook_info.pending_update_count > 0:
                print(f"⚠️  There are {webhook_info.pending_update_count} pending updates")
            if webhook_info.last_error_message:
                print(f"❌ Last error: {webhook_info.last_error_message}")
        else:
            print("❌ Webhook is NOT SET")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_webhook())
